from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

class TimeEntryCreate(BaseModel):
    project_id: uuid.UUID
    deliverable_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    started_at: Optional[datetime] = None  # If null, backend sets to now()
    is_billable: bool = True
    hourly_rate_cents: Optional[int] = None

class TimeEntryManualCreate(BaseModel):
    project_id: uuid.UUID
    deliverable_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    started_at: datetime
    ended_at: datetime
    is_billable: bool = True
    hourly_rate_cents: Optional[int] = None

class TimeEntryUpdate(BaseModel):
    description: Optional[str] = None
    is_billable: Optional[bool] = None
    hourly_rate_cents: Optional[int] = None

class TimeEntryRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    deliverable_id: Optional[uuid.UUID]
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
