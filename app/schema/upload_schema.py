from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, PositiveInt


class UploadAcceptedResponse(BaseModel):
    upload_id: str
    stored_filename: str
    size_in_bytes: PositiveInt
    status: str


class DocumentResponse(BaseModel):
    id: UUID
    original_filename: str
    status: str
    upload_time: datetime
    extracted_text: str | None = None
