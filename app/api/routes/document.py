from datetime import datetime, timezone
import os
from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document, DocumentStatus
from app.models.document_content import DocumentContent
from app.schema.upload_schema import DocumentResponse, UploadAcceptedResponse
from app.services.upload_service import process_document, save_file_to_disk

router = APIRouter()


@router.get('/documents/{document_id}', response_model=DocumentResponse)
def get_document(document_id: UUID, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="document not found")

    document_content = db.query(DocumentContent).filter(
        DocumentContent.document_id == document_id
    ).first()

    return {
        "id": document.id,
        "original_filename": document.original_filename,
        "status": document.status.value if document.status else None,
        "upload_time": document.upload_time,
        "extracted_text": document_content.extracted_text if document_content else None,
        "structured_data": document_content.structured_data if document_content else None
    }


@router.get('/docuemnts')
def get_all_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()

    return [
        {
            "id": doc.id,
            "original_filename": doc.original_filename,
            "status": doc.status.value,
            "uploaded_at": doc.upload_time,
        }
        for doc in documents
    ]


@router.post('/uploadfile', response_model=UploadAcceptedResponse)
async def create_upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
):
    try:
        temp_id = uuid4()
        file_info = await save_file_to_disk(file, temp_id)

        new_document = Document(
            original_filename=file.filename,
            stored_filename=file_info["stored_filename"],
            size_in_bytes=file_info["size_in_bytes"],
            content_type=file.content_type or "application/octet-stream",
            status=DocumentStatus.uploaded,
            upload_time=datetime.now(timezone.utc),
        )

        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        result = process_document(
        file_info["file_path"],
        new_document.id,
        )
        print(result)
        return {
            "upload_id": str(new_document.id),
            "stored_filename": file_info["stored_filename"],
            "size_in_bytes": file_info["size_in_bytes"],
            "status": new_document.status.value,
            "extracted_text": result.get("extracted_text", ""),
            "structured_data": result.get("structured_data", {}),
        }

    except Exception as e:
        db.rollback()

        if "file_info" in locals():
            file_path = file_info["file_path"]
            if os.path.exists(file_path):
                os.remove(file_path)

        raise HTTPException(status_code=500, detail=str(e))
