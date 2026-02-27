from fastapi import FastAPI
from app.database import Base, engine
import uvicorn
from config.configuration import read_yaml
from app.api.routes import document
from app.api.routes import chat
from app.models.document import Document
from app.models.document_content import DocumentContent
from dotenv import load_dotenv
load_dotenv()
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/home")
def home():
    return {"message": "welcome to DocuParse project"}

app.include_router(document.router, prefix='/api', tags=['documents'])
app.include_router(chat.router, prefix='/api', tags=['chat'])

if __name__ == "__main__":
    config = read_yaml("params.yaml")
    host = config.get("host", "localhost")
    port = config.get("port", 8000)
    uvicorn.run(app, host=host, port=port)

