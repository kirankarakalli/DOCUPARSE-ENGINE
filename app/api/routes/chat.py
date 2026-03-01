from fastapi import APIRouter
from pydantic import BaseModel
from app.genai.rag_chain import create_rag_chain

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    session_id: str


@router.post("/chat/{document_id}")
def chat_with_document(document_id: str, request: ChatRequest):
    chain = create_rag_chain(document_id)
    response = chain.invoke(
        {"input": request.question},
        config={"configurable": {"session_id": request.session_id}},
    )
    return {"response": response['answer'],
            "sources":response['sources']}
