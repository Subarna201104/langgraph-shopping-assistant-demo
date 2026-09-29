"""Run with: python -m streamlit run app.py"""

import os
from uuid import uuid4

import streamlit as st
from dotenv import load_dotenv

from bot import ask, build_graph


load_dotenv()
st.set_page_config(page_title="Shop Assistant | LangGraph", page_icon="🛍️")
st.title("🛍️ Shop Assistant")
st.caption("A small LangGraph learning project with fictional products and orders.")

with st.sidebar:
    mode_label = st.radio("Choose a mode", ["Demo (no key needed)", "AI (API key needed)"])
    st.info("Demo uses rules and sample data. AI uses a language model, tools, and a review step.")
    st.markdown("**Try asking:**")
    st.markdown("- What is the price of the Nova headphones?\n- Where is order ORD1001?\n- Summarize our chat")
    new_chat = st.button("Start a new chat")

mode = "ai" if mode_label.startswith("AI") else "demo"
if st.session_state.get("mode") != mode or new_chat:
    st.session_state.mode = mode
    st.session_state.thread_id = str(uuid4())
    st.session_state.chat = []

if mode == "ai" and not os.getenv("OPENAI_API_KEY"):
    st.warning("Add OPENAI_API_KEY to a local .env file, then restart the app. The README shows how.")
    st.stop()


@st.cache_resource
def graph_for(selected_mode: str):
    return build_graph(selected_mode)


for role, content in st.session_state.chat:
    with st.chat_message(role):
        st.write(content)

if question := st.chat_input("Type a product or order question..."):
    with st.chat_message("user"):
        st.write(question)
    try:
        with st.spinner("Thinking..."):
            answer = ask(graph_for(mode), question, st.session_state.thread_id)
    except Exception as error:
        st.error(f"The request did not finish: {error}")
    else:
        st.session_state.chat.extend([("user", question), ("assistant", answer)])
        with st.chat_message("assistant"):
            st.write(answer)

