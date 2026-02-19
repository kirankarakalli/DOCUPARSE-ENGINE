from datetime import datetime
from fastapi import Depends, FastAPI,File,UploadFile,HTTPException
from app.models.document import Document
from app.schema.upload_schema import UploadResponse
from app.services.upload_service import save_file
from app.database import Base, SessionLocal,engine
import uvicorn
from app.database import get_db
from app.models.document import Document
from app.models.document_content import DocumentContent
from sqlalchemy.orm import Session
app = FastAPI()
import os
from config.configuration import read_yaml
Base.metadata.create_all(bind=engine)
config_path=read_yaml("params.yaml")
uploads_dir = config_path.get("uploads_dir")
@app.get("/home")
def func():
    return {"message": "welcome to DocuParse project"}


@app.post("/uploadfile", response_model=UploadResponse)
async def create_upload_file(file: UploadFile = File(...),db:Session=Depends(get_db)):
    

    try:
        new_document=Document(
        original_filename=file.filename,  
        stored_filename=  "",
        size_in_bytes=  0,
        content_type=file.content_type ,
        upload_time=  datetime.utcnow(),
        )

        db.add(new_document)
        db.flush()
    
    
        file_info = await save_file(file,new_document.id)
        new_document.stored_filename = file_info["stored_filename"]
        new_document.size_in_bytes = file_info["size_in_bytes"]
        

        document_content=DocumentContent(
            document_id=new_document.id,
            extracted_text=file_info["extracted_text"]
        )
        db.add(document_content)
        db.commit()
    except Exception as e:
        db.rollback()
        if "file_info" in locals():
            file_path = os.path.join(uploads_dir, file_info["stored_filename"])
            if os.path.exists(file_path):
                os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

    return {
        **file_info,
        "upload_id": str(new_document.id)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

