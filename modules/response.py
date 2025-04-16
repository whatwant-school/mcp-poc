import asyncio
from langchain_core.messages import HumanMessage
from modules.message import to_lc_messages

# AI 모델의 스트리밍 응답 생성
def get_response(model, chat_history, user_message):
    messages = to_lc_messages(chat_history)
    messages.append(HumanMessage(content=user_message))
    # LangChain 모델의 astream 지원 시 스트리밍
    if hasattr(model, 'astream'):
        async def stream():
            async for chunk in model.astream(messages):
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
                elif isinstance(chunk, str):
                    yield chunk
        return stream()
    # 지원하지 않으면 전체 응답 반환
    async def once():
        response = await model.ainvoke(messages)
        yield response.content
    return once()

# Streamlit에서 사용할 스트리밍 제너레이터
def stream_response(model, chat_history, user_message):
    async def async_chunks():
        async for chunk in get_response(model, chat_history, user_message):
            yield chunk
    agen = async_chunks()
    while True:
        try:
            chunk = asyncio.get_event_loop().run_until_complete(agen.__anext__())
            yield chunk
        except StopAsyncIteration:
            break
