from datetime import datetime
from fastapi import UploadFile
from fastapi import HTTPException
from config.configuration import read_yaml
import os
import uuid
from app.utils.logging import logger

config_path=read_yaml("params.yaml")
uploads_dir = config_path.get("uploads_dir")
allowed_extensions = [ext.lower() for ext in config_path.get("allowed_extensions")]
max_file_size_bytes = config_path.get("max_file_size_bytes")


async def save_file(file: UploadFile):
    
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
    else:
        ext=os.path.splitext(file.filename)[1]
        file_path=os.path.join(uploads_dir, f"{unique_id}{ext}")
        with open(file_path, "wb") as f:
            f.write(content)
        logger.info(f"File uploaded successfully: {file.filename}")
        return {"upload_id": unique_id,"original_filename": file.filename, "stored_filename": f"{unique_id}{ext}", "size_in_bytes": len(content), "content_type": file.content_type, "upload_time": datetime.now()}
    