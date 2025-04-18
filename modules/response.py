import asyncio
import streamlit as st
from langchain_core.messages import HumanMessage
from modules.message import to_lc_messages

def get_response(model, chat_history, user_message):
    messages = to_lc_messages(chat_history)
    messages.append(HumanMessage(content=user_message))
    if hasattr(model, 'astream'):
        async def stream():
            async for chunk in model.astream(messages):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
                elif isinstance(chunk, str):
                    yield chunk
        return stream()
    async def once():
        response = await model.ainvoke(messages)
        yield response.content
    return once()

def stream_response(model, chat_history, user_message):
    async def async_chunks():
        async for chunk in get_response(model, chat_history, user_message):
            yield chunk
    agen = async_chunks()
    loop = getattr(st.session_state, "event_loop", None)
    if loop is None or loop.is_closed():
        loop = asyncio.new_event_loop()
        st.session_state.event_loop = loop
    while True:
        try:
            chunk = loop.run_until_complete(agen.__anext__())
            yield chunk
        except StopAsyncIteration:
            break
