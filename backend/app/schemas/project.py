from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

class ProjectCreate(BaseModel):
    client_id: uuid.UUID
    name: str
    description: Optional[str] = None
    default_hourly_rate_cents: Optional[int] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    onboarding_video_url: Optional[str] = None
    onboarding_message: Optional[str] = None
    show_onboarding: Optional[bool] = None
    default_hourly_rate_cents: Optional[int] = None

class ProjectRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    client_id: uuid.UUID
    name: str
    description: Optional[str]
    status: str
    onboarding_video_url: Optional[str]
    onboarding_message: Optional[str]
    show_onboarding: bool
    default_hourly_rate_cents: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
