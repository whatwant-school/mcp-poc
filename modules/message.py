import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string
import tiktoken

# GPT 모델 토큰 수 계산
def count_gpt_tokens(text, model_name="gpt-4o"):
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

# Gemini 모델 토큰 수 추정
def estimate_gemini_tokens(text):
    return int(len(text) / 4)

# 채팅 이력 -> LangChain 메시지 포맷 변환
def to_lc_messages(chat_history):
    messages = []
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages

# 채팅 이력 UI 표시
def display_chat_history():
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 채팅 이력 및 토큰 초기화
def clear_chat_history():
    st.session_state.chat_history = []
    st.session_state.token_usage = 0
    st.rerun()

# 사용자 입력 추가
def add_user_input(prompt):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# 채팅 이력 토큰 계산
def calculate_tokens(model_name, chat_history):
    buffer = get_buffer_string(to_lc_messages(chat_history))
    if model_name == "Gemini":
        st.session_state.token_usage = estimate_gemini_tokens(buffer)
    else:
        st.session_state.token_usage = count_gpt_tokens(buffer, model_name)
