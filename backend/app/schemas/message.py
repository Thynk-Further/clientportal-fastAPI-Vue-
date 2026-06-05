import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class MessageRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    deliverable_id: Optional[uuid.UUID] = None
    sender_type: str
    sender_user_id: Optional[uuid.UUID] = None
    sender_client_id: Optional[uuid.UUID] = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
