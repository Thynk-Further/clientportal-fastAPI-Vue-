from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from typing import Optional

class ApprovalCreate(BaseModel):
    action: str
    comment: Optional[str] = None

class ApprovalRead(BaseModel):
    id: uuid.UUID
    deliverable_id: uuid.UUID
    client_id: uuid.UUID
    action: str
    comment: Optional[str]
    client_ip: Optional[str]
    client_user_agent: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
