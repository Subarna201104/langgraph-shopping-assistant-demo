"""Optional first AI exercise: a ReAct-style agent that can use a calculator tool."""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


@tool
def calculate_total(unit_price: int, quantity: int) -> int:
    """Multiply an item's rupee price by the number of items to buy."""
    return unit_price * quantity


def main() -> None:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("Add OPENAI_API_KEY to .env first. The no-key Demo app works without it.")
        return

    agent = create_agent(
        model=ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-5-nano")),
        tools=[calculate_total],
        system_prompt="You are a helpful shop assistant. Use the calculator tool for multiplication.",
    )
    result = agent.invoke({"messages": [{"role": "user", "content": "A mouse is ₹899. How much do 3 cost?"}]})
    for message in result["messages"]:
        if getattr(message, "tool_calls", None):
            print("Agent called tool:", message.tool_calls)
        if message.type == "tool":
            print("Tool returned:", message.content)
    print("Final answer:", result["messages"][-1].content)


if __name__ == "__main__":
    main()

