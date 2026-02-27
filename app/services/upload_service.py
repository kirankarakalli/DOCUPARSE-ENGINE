from datetime import datetime
from fastapi import UploadFile
import aiofiles
from fastapi import HTTPException
from app.models.document_content import DocumentContent
from app.services.document_parser.pdf_parser import parse_pdf
from config.configuration import read_yaml
import os
import uuid
from sqlalchemy import UUID
from app.utils.logging import logger
from app.services.preprocessing_pipeline.preprocess import preprocess_image
from app.services.preprocessing_pipeline.ocr import extract_text_from_image
import asyncio
from app.database import SessionLocal
from app.models.document import Document, DocumentStatus
from app.services.llm.extraction_service import extract_structured_data
from app.services.validator.validator_factory import get_validator
from app.services.validator.schema_validator import validate_against_schema,SCHEMA
from app.genai.indexer import index_documents
config=read_yaml("params.yaml")
uploads_dir = config.get("uploads_dir")
if not uploads_dir:
    raise ValueError("uploads_dir not found in configuration")
allowed_extensions = [ext.lower() for ext in config.get("allowed_extensions", [])]
if not allowed_extensions:
    raise ValueError("allowed_extensions not found in configuration")
max_file_size_bytes = config.get("max_file_size_bytes")
if not max_file_size_bytes:
    raise ValueError("max_file_size_bytes not found in configuration")

async def save_file_to_disk(file: UploadFile,document_id:UUID):

    os.makedirs(uploads_dir, exist_ok=True)
    
    file_extension = os.path.splitext(file.filename)[1].lower().replace(".", "")
    content = await file.read()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")


    if len(content) > max_file_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds {max_file_size_bytes} bytes limit"
        )
    
    file_path=os.path.join(uploads_dir, f"{document_id}.{file_extension}")
    if not os.path.abspath(file_path).startswith(os.path.abspath(uploads_dir)):
        raise HTTPException(status_code=400, detail="Invalid file path")
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)
    
    return {
        "stored_filename": f"{document_id}.{file_extension}",
        "size_in_bytes": len(content),
        "file_path":file_path
    }

    
def process_document(file_path: str, document_id: UUID):
    db = SessionLocal()
    document = None

    try:
        logger.info(f"Started processing document {document_id}")

        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError("Document not found")

        document.status = DocumentStatus.preprocessing
        db.commit()

        file_extension = os.path.splitext(file_path)[1].lower()

        # PDF handling
        if file_extension == ".pdf":
            extracted_text = parse_pdf(file_path)

        # Image handling
        else:
            preprocess_result = preprocess_image(file_path, str(document_id))
            deskewed_path = preprocess_result.get("deskewed")

            if not deskewed_path:
                raise ValueError("Deskewed path missing")

            extracted_text = extract_text_from_image(deskewed_path)

        structured_data=extract_structured_data(extracted_text)
        print(structured_data)
        validator=get_validator(structured_data.get('document_type'))
        if validator:
            is_valid,error=validator.validate(structured_data)
            if not is_valid:
                document.status = DocumentStatus.failed
                logger.error(f"Validation failed: {error}")
        
        is_valid_schema,schema_error=validate_against_schema(structured_data,SCHEMA)

        if not is_valid_schema:
            raise ValueError(f"Schema validation failed: {schema_error}")

        existing = db.query(DocumentContent).filter(
            DocumentContent.document_id == document_id
        ).first()

        if existing:
            existing.extracted_text = extracted_text
            existing.structured_data= structured_data
        else:
            db.add(DocumentContent(
                document_id=document_id,
                extracted_text=extracted_text,
                structured_data=structured_data
                
            ))

        document.status = DocumentStatus.completed
        db.commit()
        print("TYPE OF extracted_text:", type(extracted_text))
        index_documents(document_id, extracted_text)
        logger.info(f"Completed processing document {document_id}")

    except Exception as e:
        db.rollback()

        if document:
            document.status = DocumentStatus.failed
            db.commit()

        logger.error(f"OCR processing failed: {str(e)}")

    finally:
        db.close()





