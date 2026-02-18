from pydantic import BaseModel
from datetime import datetime

class UploadResponse(BaseModel):
    upload_id: str
    original_filename: str
    stored_filename: str
    size_in_bytes: int
    content_type: str
    upload_time: datetime
    extracted_text: str


