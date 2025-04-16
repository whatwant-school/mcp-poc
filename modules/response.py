from langchain_core.messages import HumanMessage
from modules.message import convert_history_to_messages

# Generate a response using the AI model
async def get_response(model, chat_history, user_message):
    messages = convert_history_to_messages(chat_history)  # Convert chat history to LangChain format
    messages.append(HumanMessage(content=user_message))  # Add user message
    response = await model.ainvoke(messages)  # Generate response asynchronously
    return response.content
