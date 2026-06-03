from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from typing import Optional

class TimeEntryStart(BaseModel):
    project_id: uuid.UUID
    deliverable_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    is_billable: bool = True

class TimeEntryManual(BaseModel):
    project_id: uuid.UUID
    deliverable_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    started_at: datetime
    ended_at: datetime
    is_billable: bool = True

class TimeEntryRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    deliverable_id: Optional[uuid.UUID] = None
    user_id: uuid.UUID
    description: Optional[str]
    started_at: datetime
    ended_at: Optional[datetime]
    duration_seconds: Optional[int]
    is_billable: bool
    hourly_rate_cents: Optional[int]
    invoice_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
