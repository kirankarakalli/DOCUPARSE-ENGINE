from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.genai.vector_store import create_vector_store
from app.genai.memory import get_session_memory


def create_rag_chain(document_id: str):

    vector_store = create_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 4,
            "filter": {"document_id": str(document_id)},
        }
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    contextualize_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Rewrite the user's question into a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    contextualize_chain = contextualize_prompt | llm | StrOutputParser()

    history_aware_retriever = contextualize_chain | retriever

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant.\n"
                "Answer ONLY using the provided context.\n"
                "If the answer is not in the context, say 'I don't know.'",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "Context:\n{context}\n\nQuestion:\n{input}"),
        ]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": history_aware_retriever | RunnableLambda(format_docs),
            "input": RunnableLambda(lambda x: x["input"]),
            "chat_history": RunnableLambda(lambda x: x["chat_history"]),
        }
        | qa_prompt
        | llm
        | StrOutputParser()
    )

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return conversational_rag_chain
