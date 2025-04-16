import asyncio
import nest_asyncio
import streamlit as st

from modules.llm_client import get_openai_response, get_gemini_response

nest_asyncio.apply()

# 전역 이벤트 루프 생성
if "event_loop" not in st.session_state:
    loop = asyncio.new_event_loop()
    st.session_state.event_loop = loop
    asyncio.set_event_loop(loop)

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Streamlit 앱의 페이지 설정 구성
st.set_page_config(page_title="WHATWANT Chat", layout="wide")
st.title("💬 와던트 채팅 봇")


# 사용할 AI 모델을 선택하는 사이드바
model_name = st.sidebar.selectbox(
    "🧠 사용할 AI 모델을 선택하세요",
    ["GPT-4", "GPT-3.5", "Gemini", "Custom-Bot"]
)

# 현재 선택된 모델을 사이드바에 표시e
st.sidebar.markdown(f"현재 선택된 모델: **{model_name}**")



# 세션 상태에 저장된 모든 이전 채팅 메시지 표시
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# 채팅 입력 상자에서 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요"):

    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 선택된 모델에 따라 응답 생성
    if model_name == "Gemini":
        response = get_gemini_response(prompt)
    elif model_name == "GPT-4":
        response = get_openai_response(prompt, model="gpt-4")
    else:
        response = get_openai_response(prompt, model="gpt-3.5-turbo")

    # 어시스턴트의 응답을 세션 상태에 추가
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
