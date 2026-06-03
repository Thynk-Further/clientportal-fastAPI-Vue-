from pydantic import BaseModel
import uuid
from datetime import datetime

class PresignedUrlRequest(BaseModel):
    filename: str
    content_type: str
    deliverable_id: uuid.UUID

class PresignedUrlResponse(BaseModel):
    presigned_url: str
    object_key: str

class FileUploadCreate(BaseModel):
    object_key: str
    deliverable_id: uuid.UUID
    file_size: int
    mime_type: str

class FileUploadRead(BaseModel):
    id: uuid.UUID
    deliverable_id: uuid.UUID
    uploaded_by_user_id: uuid.UUID
    file_name: str
    file_url: str
    object_key: str
    file_size: int
    mime_type: str
    created_at: datetime

    class Config:
        from_attributes = True
