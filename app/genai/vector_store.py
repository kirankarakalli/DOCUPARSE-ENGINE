from app.genai.embeddings import get_embeddings
from langchain_chroma import Chroma
PERSIST_DIRECTORY = "./chroma_db"

def create_vector_store():
    embeddings=get_embeddings()
    return Chroma(
        collection_name="genai_collection",
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )