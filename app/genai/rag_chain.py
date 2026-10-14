from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.genai.vector_store import create_vector_store
from app.genai.memory import get_session_memory


def create_rag_chain(document_ids: list[str]):

    vector_store = create_vector_store()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)

    contextualize_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Rewrite the user's question into a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    contextualize_chain = contextualize_prompt | llm | StrOutputParser()

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

    def retrieve_docs(inputs):
        standalone_question = contextualize_chain.invoke(inputs)

        docs_with_scores = vector_store.similarity_search_with_score(
            query=standalone_question,
            k=4,
            filter={"document_id": {"$in": document_ids}},
        )

        docs = [doc for doc, score in docs_with_scores]

        context_text = "\n\n".join(doc.page_content for doc in docs)

        return {
            "context": context_text,
            "input": inputs["input"],
            "chat_history": inputs["chat_history"],
            "docs_with_scores": docs_with_scores,
        }

    def calculate_confidence(docs_with_scores):
        if not docs_with_scores:
            return 0.0

        avg_distance = sum(score for _, score in docs_with_scores) / len(docs_with_scores)

        confidence = 1 / (1 + avg_distance)
        
        return round(confidence, 2)

        return round(confidence, 2)

    def format_output(inputs):
        answer = (qa_prompt | llm | StrOutputParser()).invoke(inputs)

        confidence = calculate_confidence(inputs["docs_with_scores"])

        return {
            "answer": answer,
            "sources": [
                {
                    "content_preview": doc.page_content[:200],
                    "metadata": doc.metadata,
                }
                for doc, _ in inputs["docs_with_scores"]
            ],
            "confidence": confidence,
        }

    rag_chain = (
        RunnableLambda(retrieve_docs)
        | RunnableLambda(format_output)
    )

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_memory,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain