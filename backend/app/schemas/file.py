from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from typing import Optional

class PresignedUrlRequest(BaseModel):
    deliverable_id: uuid.UUID
    filename: str
    content_type: str

class PresignedUrlResponse(BaseModel):
    presigned_url: str
    object_key: str

class FileUploadConfirm(BaseModel):
    deliverable_id: uuid.UUID
    object_key: str
    file_size: int
    mime_type: str
    file_name: str

class FileUploadRead(BaseModel):
    id: uuid.UUID
    deliverable_id: uuid.UUID
    uploaded_by_user_id: uuid.UUID
    file_name: str
    file_url: Optional[str] = None
    object_key: str
    file_size: int
    mime_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
