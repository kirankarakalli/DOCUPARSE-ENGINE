from datetime import datetime
from fastapi import UploadFile
import aiofiles
from fastapi import HTTPException
from config.configuration import read_yaml
import os
import uuid
from app.utils.logging import logger
from app.services.preprocessing_pipeline.preprocess import preprocess_image
from app.services.preprocessing_pipeline.ocr import extract_text_from_image
import asyncio
from app.database import SessionLocal
from app.models.document import Document

config_path=read_yaml("params.yaml")
uploads_dir = config_path.get("uploads_dir")
allowed_extensions = [ext.lower() for ext in config_path.get("allowed_extensions")]
max_file_size_bytes = config_path.get("max_file_size_bytes")


async def save_file(file: UploadFile,document_id:str):
    
    os.makedirs(uploads_dir, exist_ok=True)
    unique_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1].lower().replace(".", "")

    if file_extension not in allowed_extensions:
        logger.warning(f"Invalid file type: {file_extension}")
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    content = await file.read()

    if len(content) > max_file_size_bytes:  
        logger.warning(f"File size exceeds limit: {len(content)} bytes")
        raise HTTPException(status_code=413, detail=f"File size exceeds {max_file_size_bytes} bytes limit")
    
    file_path=os.path.join(uploads_dir, f"{document_id}.{file_extension}")
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)
        
    try:
        preprocess_file = await asyncio.to_thread(preprocess_image, file_path, unique_id)
        deskew_path = preprocess_file.get("deskewed")
        if not deskew_path:
            raise ValueError("deskewed path is missing")
        extract_text = await asyncio.to_thread(extract_text_from_image, deskew_path)
        
    except Exception as e:
        logger.error(f"Error in preprocessing/OCR: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing file")
    
    logger.info(f"File uploaded successfully: {file.filename}")
    return {
        "upload_id": unique_id,
        "original_filename": file.filename,
        "stored_filename": f"{unique_id}.{file_extension}",
        "size_in_bytes": len(content),
        "content_type": file.content_type,
        "upload_time": datetime.now().isoformat(),
        "extracted_text": extract_text
    }

    