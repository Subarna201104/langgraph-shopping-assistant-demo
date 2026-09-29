"""A LangGraph router with product, order, summary, and general nodes."""

import os
import re
from typing import Literal

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import BaseModel, Field

from shop_data import get_order_status, order_lookup, product_search, search_products


class ShopState(MessagesState):
    route: str


class RouteChoice(BaseModel):
    destination: Literal["products", "orders", "summary", "general"] = Field(
        description="The one specialist best suited to the latest user message."
    )


def message_text(message) -> str:
    """Turn a normal or block-based model response into displayable text."""
    if isinstance(message.content, str):
        return message.content
    return "\n".join(
        item.get("text", "") for item in message.content if isinstance(item, dict)
    ).strip()


def latest_question(state: ShopState) -> str:
    return next(
        (message_text(m) for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        "",
    )


def build_graph(mode: Literal["demo", "ai"] = "demo"):
    """Compile a graph. Demo uses rules; AI uses real model calls and tools."""
    if mode not in {"demo", "ai"}:
        raise ValueError("Mode must be 'demo' or 'ai'.")

    model = None
    product_agent = None
    order_agent = None
    if mode == "ai":
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("AI mode needs OPENAI_API_KEY in .env. Use Demo mode without a key.")
        model = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-5-nano"))
        product_agent = create_agent(
            model=model,
            tools=[search_products],
            system_prompt=(
                "You help with the fictional shop's products. Always use search_products "
                "before giving product facts. Answer only from its result; say when unknown. "
                "Be brief and helpful. These products are samples, not real listings."
            ),
        )
        order_agent = create_agent(
            model=model,
            tools=[get_order_status],
            system_prompt=(
                "You help with fictional sample orders. Ask for an order ID if missing. "
                "Always call get_order_status before stating a status or delivery date. "
                "Do not invent statuses or dates. Be brief."
            ),
        )

    def route_message(state: ShopState) -> dict:
        question = latest_question(state).lower()
        if mode == "ai":
            recent = state["messages"][-8:]
            decision = model.with_structured_output(RouteChoice).invoke(
                [
                    SystemMessage(content=(
                        "Choose exactly one route for the latest user request: products for item "
                        "questions, orders for delivery/status, summary for summarizing this chat, "
                        "general for greetings or anything else. Use context for follow-up questions."
                    )),
                    *recent,
                ]
            )
            return {"route": decision.destination}

        if any(word in question for word in ("summarize", "summary", "recap")):
            route = "summary"
        elif re.search(r"\bord\d{4}\b", question) or any(
            word in question for word in ("order", "delivery", "delivered", "shipped", "tracking")
        ):
            route = "orders"
        elif any(word in question for word in (
            "product", "headphone", "keyboard", "laptop", "mouse", "price", "warranty", "stock"
        )):
            route = "products"
        elif question in {"hi", "hello", "hey"}:
            route = "general"
        else:
            route = state.get("route", "general")
        return {"route": route}

    def product_node(state: ShopState) -> dict:
        if mode == "ai":
            result = product_agent.invoke({"messages": state["messages"][-10:]})
            return {"messages": [AIMessage(content=message_text(result["messages"][-1]))]}
        question = latest_question(state)
        facts = product_search(question)
        if facts.startswith("No matching"):
            for message in reversed(state["messages"][:-1]):
                if isinstance(message, HumanMessage):
                    facts = product_search(message_text(message))
                    if not facts.startswith("No matching"):
                        break
        return {"messages": [AIMessage(content=facts + "\n\n(Demo uses sample data.)")]}

    def order_node(state: ShopState) -> dict:
        if mode == "ai":
            result = order_agent.invoke({"messages": state["messages"][-10:]})
            return {"messages": [AIMessage(content=message_text(result["messages"][-1]))]}
        questions = " ".join(
            message_text(m) for m in state["messages"] if isinstance(m, HumanMessage)
        )
        ids = re.findall(r"\bORD\d{4}\b", questions, flags=re.IGNORECASE)
        reply = order_lookup(ids[-1]) if ids else "Please enter a sample order ID: ORD1001, ORD1002, or ORD1003."
        return {"messages": [AIMessage(content=reply + "\n\n(Demo uses sample orders.)")]}

    def summary_node(state: ShopState) -> dict:
        recent = state["messages"][-14:-1]
        if mode == "ai":
            draft = model.invoke([
                SystemMessage(content="Summarize this conversation in 2–4 short bullets. Use only facts in the messages."),
                *recent,
            ])
            reviewed = model.invoke([
                SystemMessage(content="Review the proposed summary against this conversation. Correct invented or missing facts. Return only the final 2–4 bullets."),
                *recent,
                HumanMessage(content="Proposed summary:\n" + message_text(draft)),
            ])
            return {"messages": [AIMessage(content=message_text(reviewed))]}
        prior_questions = [message_text(m) for m in recent if isinstance(m, HumanMessage)]
        reply = "You asked about:\n" + "\n".join(f"• {q}" for q in prior_questions[-4:]) if prior_questions else "We have not discussed anything yet."
        return {"messages": [AIMessage(content=reply + "\n\n(Demo summary; AI mode drafts and reviews.)")]}

    def general_node(state: ShopState) -> dict:
        if mode == "ai":
            reply = model.invoke([
                SystemMessage(content="You are a concise assistant for a fictional shop. Help users ask about products or sample orders. Do not invent shop facts."),
                *state["messages"][-8:],
            ])
            return {"messages": [AIMessage(content=message_text(reply))]}
        return {"messages": [AIMessage(content="Hi! Ask me about headphones, a keyboard, a laptop stand, a mouse, or sample order ORD1001. You can also ask for a chat summary.")]}

    graph = StateGraph(ShopState)
    graph.add_node("router", route_message)
    graph.add_node("products", product_node)
    graph.add_node("orders", order_node)
    graph.add_node("summary", summary_node)
    graph.add_node("general", general_node)
    graph.add_edge(START, "router")
    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {name: name for name in ("products", "orders", "summary", "general")},
    )
    for name in ("products", "orders", "summary", "general"):
        graph.add_edge(name, END)
    # A thread_id lets the same conversation remember earlier turns while the app runs.
    return graph.compile(checkpointer=InMemorySaver())


def ask(graph, question: str, thread_id: str) -> str:
    result = graph.invoke(
        {"messages": [HumanMessage(content=question)]},
        {"configurable": {"thread_id": thread_id}},
    )
    return message_text(result["messages"][-1])

