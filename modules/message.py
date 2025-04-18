import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string
import tiktoken

def count_gpt_tokens(text, model_name="gpt-4o"):
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

def estimate_gemini_tokens(text):
    return int(len(text) / 4)

def to_lc_messages(chat_history):
    messages = []
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages

def display_chat_history():
    history = st.session_state.chat_history
    for msg in history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

def clear_chat_history():
    st.session_state.chat_history = []
    st.session_state.token_usage = 0
    st.rerun()

def add_user_input(prompt):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

def calculate_tokens(model_name, chat_history):
    buffer = get_buffer_string(to_lc_messages(chat_history))
    if model_name == "Gemini":
        st.session_state.token_usage = estimate_gemini_tokens(buffer)
    else:
        st.session_state.token_usage = count_gpt_tokens(buffer, model_name)
