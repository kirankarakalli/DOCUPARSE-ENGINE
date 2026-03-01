from fastapi import APIRouter
from pydantic import BaseModel
from app.genai.rag_chain import create_rag_chain

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    session_id: str
    document_id: list[str]


@router.post("/chat")
def chat_with_document(request: ChatRequest):
    chain = create_rag_chain(request.document_id)
    response = chain.invoke(
        {"input": request.question},
        config={"configurable": {"session_id": request.session_id}},
    )
    return {"response": response['answer'],
            "sources":response['sources'],
            "confidence": response['confidence']}
