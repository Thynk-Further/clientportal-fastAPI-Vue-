from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
import uuid

class NotificationRead(BaseModel):
    id: uuid.UUID
    notification_type: str
    entity_type: str
    entity_id: uuid.UUID
    title: str
    message: str
    link_url: Optional[str]
    read_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationListResponse(BaseModel):
    items: List[NotificationRead]
    unread_count: int
