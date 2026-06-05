from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    company_name: Optional[str] = None

class ClientReadList(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    email: EmailStr
    company_name: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ClientReadDetail(ClientReadList):
    portal_token: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class ClientMemberCreate(BaseModel):
    name: str
    email: EmailStr

class ClientMemberRead(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    name: str
    email: EmailStr
    member_token: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
