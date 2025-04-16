import os
from openai import OpenAI
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


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