from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2:3b")

template = """
You are a helpful assistant for our restaurant.

Use the restaurant reviews and previous conversation to answer naturally.

Previous Conversation:
{chat_history}

Restaurant Reviews:
{reviews}

Current Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model


def format_chat_history(chats):

    if not chats:
        return "No previous conversation."

    conversation = []

    for chat in chats:

        conversation.append(
            f"User: {chat['question']}"
        )

        conversation.append(
            f"Assistant: {chat['answer']}"
        )

    return "\n".join(conversation)


def get_ai_response(question, chats):

    reviews = retriever.invoke(question)

    chat_history = format_chat_history(chats)

    response = chain.invoke(
        {
            "reviews": reviews,
            "question": question,
            "chat_history": chat_history
        }
    )

    return response