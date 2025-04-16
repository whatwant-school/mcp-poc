import streamlit as st
import asyncio
import nest_asyncio
from dotenv import load_dotenv

# Custom module imports
from modules.config import init_session_state, get_chat_model, render_model_selection, get_model_name
from modules.message import display_chat_history, add_user_input, calculate_tokens, clear_chat_history
from modules.response import get_response

# Load environment variables and apply asyncio patch
load_dotenv()
nest_asyncio.apply()

# Streamlit page configuration
st.set_page_config(page_title="WHATWANT Chat", layout="wide")

st.title("💬 WHATWANT Chatting Bot")

# Sidebar branding
st.sidebar.markdown("### ✍️ Made by [WHATWANT](https://www.whatwant.com) 🚀")
st.sidebar.divider()

# Initialize session state
init_session_state()

# Render model selection menu
render_model_selection()

# Initialize chat model
model_name = get_model_name()
st.session_state.chat_model = get_chat_model(model_name)
st.sidebar.markdown(f"현재 선택된 모델: **{model_name}**")

# Display chat history in the UI
display_chat_history()

# Handle user input
if user_input := st.chat_input("메시지를 입력하세요"):
    add_user_input(user_input)  # Add user input to chat history
    response = asyncio.get_event_loop().run_until_complete(
        get_response(st.session_state.chat_model, st.session_state.chat_history, user_input)
    )  # Generate response using the model
    st.session_state.chat_history.append({"role": "assistant", "content": response})  # Add response to chat history
    with st.chat_message("assistant"):
        st.markdown(response)  # Display assistant response in the UI

    calculate_tokens(model_name, st.session_state.chat_history)  # Calculate token usage

# Display token usage in the sidebar
st.sidebar.divider()
st.sidebar.markdown(f"🧾 **누적 토큰 수:** `{st.session_state.token_usage}`")

# Add button to clear chat history
st.sidebar.divider()
if st.sidebar.button("💫 대화 내용 초기화", key="clear_button"):
    clear_chat_history()  # Clear chat history
