from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

class DeliverableCreate(BaseModel):
    name: str
    description: Optional[str] = None

class DeliverableUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class DeliverableRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    description: Optional[str]
    status: str
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
