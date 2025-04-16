import asyncio
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# 사이드바에 AI 모델 선택 메뉴 렌더링
def render_model_selection():
    st.session_state.model_name = st.sidebar.selectbox(
        "🧠 AI 모델 선택",
        ["Gemini", "GPT-4o", "GPT-3.5", "GPT-4.1 Nano"],
        index=0,
        key="model_selection_key"
    )

# 세션 상태 초기화
def init_session_state():
    if "event_loop" not in st.session_state:
        loop = asyncio.new_event_loop()
        st.session_state.event_loop = loop
        asyncio.set_event_loop(loop)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "token_usage" not in st.session_state:
        st.session_state.token_usage = 0
    if "model_name" not in st.session_state:
        st.session_state.model_name = "Gemini"

# 선택된 모델명에 따라 AI 모델 인스턴스 반환
def get_chat_model(name):
    if name == "Gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-pro-exp-03-25",
            temperature=0.7,
            streaming=True,
        )
    model_map = {
        "GPT-4o": "gpt-4o",
        "GPT-3.5": "gpt-3.5-turbo",
        "GPT-4.1 Nano": "gpt-4.1-nano"
    }
    return ChatOpenAI(model=model_map.get(name, "gpt-4.1-nano"), temperature=0.7, streaming=True)

# 현재 선택된 모델명 반환
def get_model_name():
    return st.session_state.get("model_name", "Gemini")
