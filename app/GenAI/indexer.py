from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.genai.vector_store import create_vector_store
from langchain_community.docstore.document import Document

def index_documents(document_id:str,text:str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    docs=[

        Document(page_content=chunk, metadata={"document_id": str(document_id)}) for chunk in chunks
    ]

    vector_store=create_vector_store()
    vector_store.add_documents(docs)  
    


