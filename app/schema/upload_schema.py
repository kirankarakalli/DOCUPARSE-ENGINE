from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, PositiveInt


class UploadAcceptedResponse(BaseModel):
    upload_id: str
    stored_filename: str
    size_in_bytes: PositiveInt
    status: str
    extracted_text: str | None = None
    structured_data: dict | None = None


class DocumentResponse(BaseModel):
    id: UUID
    original_filename: str
    status: str
    upload_time: datetime
    extracted_text: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None 

    class Config:
        from_attributes = True   
       
