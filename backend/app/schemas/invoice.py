from pydantic import BaseModel, ConfigDict
import uuid
from datetime import date, datetime
from typing import List, Optional

class InvoiceLineItem(BaseModel):
    description: str
    amount_cents: int

class InvoiceCreate(BaseModel):
    project_id: uuid.UUID
    line_items: List[InvoiceLineItem]
    amount_cents: int
    due_date: date
    time_entry_ids: Optional[List[uuid.UUID]] = []

class InvoiceRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    user_id: uuid.UUID
    client_id: uuid.UUID
    stripe_invoice_id: str
    amount_cents: int
    currency: str
    status: str
    line_items: List[dict]
    due_date: date
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class InvoicePayResponse(BaseModel):
    client_secret: str
