import streamlit as st
from dotenv import load_dotenv
from modules.config import (
    init_session_state,
    get_chat_model,
    render_model_selection,
    get_model_name,
)
from modules.message import (
    display_chat_history,
    add_user_input,
    calculate_tokens,
    clear_chat_history,
)
from modules.response import stream_response

def main():
    load_dotenv()
    st.set_page_config(page_title="WHATWANT Chat", layout="wide")
    st.title("💬 WHATWANT Chatting Bot")

    st.sidebar.markdown("### ✍️ Made by [WHATWANT](https://www.whatwant.com) 🚀")
    st.sidebar.divider()

    init_session_state()
    render_model_selection()

    selected_model = get_model_name()
    st.session_state.chat_model = get_chat_model(selected_model)
    st.sidebar.markdown(f"현재 선택된 모델: **{selected_model}**")

    display_chat_history()

    user_message = st.chat_input("메시지를 입력하세요")
    if user_message:
        add_user_input(user_message)
        with st.chat_message("assistant"):
            chunks = []
            for chunk in st.write_stream(
                stream_response(
                    st.session_state.chat_model,
                    st.session_state.chat_history,
                    user_message
                )
            ):
                chunks.append(chunk)
            assistant_reply = "".join(chunks)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
        calculate_tokens(selected_model, st.session_state.chat_history)

    st.sidebar.divider()
    st.sidebar.markdown(f"🧾 **누적 토큰 수:** `{st.session_state.token_usage}`")
    st.sidebar.divider()
    if st.sidebar.button("💫 대화 내용 초기화", key="clear_button"):
        clear_chat_history()

if __name__ == "__main__":
    main()
