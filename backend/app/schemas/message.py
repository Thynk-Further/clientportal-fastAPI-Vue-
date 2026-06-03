from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    deliverable_id: Optional[uuid.UUID] = None
    content: str

class MessageRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    deliverable_id: Optional[uuid.UUID] = None
    sender_type: str
    sender_user_id: Optional[uuid.UUID] = None
    sender_client_id: Optional[uuid.UUID] = None
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
