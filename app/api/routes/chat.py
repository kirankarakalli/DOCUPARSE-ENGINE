from fastapi import APIRouter
from pydantic import BaseModel
from app.genai.rag_chain import create_rag_chain

router = APIRouter()

class ChatRequest(BaseModel):
    document_id: str
    question: str

@router.post("/chat")
def chat_with_document(request: ChatRequest):
    chain = create_rag_chain(request.document_id)
    response = chain.invoke(request.question)
    return {"response": response}

