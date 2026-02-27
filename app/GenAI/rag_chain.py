from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.genai.vector_store import create_vector_store


def create_rag_chain(document_id: str):

    vector_store = create_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 4,
            "filter": {"document_id": str(document_id)}
        }
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful assistant.

Answer the question using ONLY the provided context.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question:
{question}
"""
    )

    # LCEL chain
    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain