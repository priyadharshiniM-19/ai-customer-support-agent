from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2:3b")

template = """
You are an expert assistant for XX Pizza Restaurant.

Answer ONLY using the restaurant reviews provided below.

Reviews:
{reviews}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model


def get_ai_response(question):
    reviews = retriever.invoke(question)

    response = chain.invoke(
        {
            "reviews": reviews,
            "question": question
        }
    )

    return response