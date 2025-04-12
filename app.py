import os
import streamlit as st
from openai import OpenAI
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

# 환경 변수에서 API 키를 가져와 OpenAI와 Google Generative AI 클라이언트 초기화
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit 앱의 페이지 설정 구성
st.set_page_config(page_title="Streamlit Chat", layout="centered")

# 사용할 AI 모델을 선택하는 사이드바
model_name = st.sidebar.selectbox(
    "🧠 사용할 AI 모델을 선택하세요",
    ["GPT-4", "GPT-3.5", "Gemini", "Custom-Bot"]
)

# 현재 선택된 모델을 사이드바에 표시
st.sidebar.markdown(f"현재 선택된 모델: **{model_name}**")

# 세션 상태에 채팅 메시지를 저장하기 위한 초기화 (초기화되지 않은 경우)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 애플리케이션의 메인 제목
st.title("💬 스트림릿 채팅 봇")

# 세션 상태에 저장된 모든 이전 채팅 메시지 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# OpenAI의 GPT 모델에서 응답을 가져오는 함수
def get_openai_response(prompt, model="gpt-3.5-turbo"):
    try:
        # OpenAI API에 채팅 완료 요청 보내기
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        # 어시스턴트의 응답 반환
        return response.choices[0].message.content.strip()
    except Exception as e:
        # API 호출 중 발생한 오류 처리 및 반환
        return f"❌ OpenAI 오류: {e}"

# Google의 Gemini 모델에서 응답을 가져오는 함수
def get_gemini_response(prompt):
    try:
        # 생성 모델 인스턴스를 생성하고 응답 생성
        model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")
        response = model.generate_content(prompt)
        # 생성된 응답 텍스트 반환
        return response.text
    except Exception as e:
        # API 호출 중 발생한 오류 처리 및 반환
        return f"❌ Gemini 오류: {e}"

# 채팅 입력 상자에서 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자의 메시지를 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
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
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
