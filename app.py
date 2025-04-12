import os
from openai import OpenAI
import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

# API 키 설정
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 페이지 기본 설정
st.set_page_config(page_title="Streamlit Chat", layout="centered")

# 사이드바에서 모델 선택
model_name = st.sidebar.selectbox(
    "🧠 사용할 AI 모델을 선택하세요",
    ["GPT-4", "GPT-3.5", "Gemini", "Custom-Bot"]
)

st.sidebar.markdown(f"현재 선택된 모델: **{model_name}**")

# 채팅 히스토리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 제목
st.title("💬 스트림릿 채팅 봇")

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# GPT 응답 함수
def get_openai_response(prompt, model="gpt-3.5-turbo"):
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ OpenAI 오류: {e}"

# Gemini 응답 함수
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini 오류: {e}"

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요"):
    # 유저 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ✅ 모델에 따라 응답 처리
    if model_name == "Gemini":
        response = get_gemini_response(prompt)
    elif model_name == "GPT-4":
        response = get_openai_response(prompt, model="gpt-4")
    else:  # GPT-3.5
        response = get_openai_response(prompt, model="gpt-3.5-turbo")

    # 응답 저장 및 출력
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
