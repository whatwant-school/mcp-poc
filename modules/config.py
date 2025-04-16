import asyncio
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# Render AI model selection menu in the sidebar
def render_model_selection():
    st.session_state.model_name = st.sidebar.selectbox(
        "🧠 Select AI Model",  # Prompt for model selection
        ["Gemini", "GPT-4", "GPT-3.5", "Custom-Bot"],  # Available models
        index=0,  # Default selection
        key="model_selection_key"  # Session state key
    )

# Initialize session state variables
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

# Get AI model instance based on the selected model name
def get_chat_model(name):
    if name == "Gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-pro-exp-03-25",
            temperature=0.7,
        )
    model_map = {
        "GPT-4": "gpt-4o",
        "GPT-3.5": "gpt-3.5-turbo",
        "Custom-Bot": "gpt-4"
    }
    return ChatOpenAI(model=model_map.get(name, "gpt-4"), temperature=0.7)

# Retrieve the currently selected model name
def get_model_name():
    return st.session_state.get("model_name", "Gemini")
