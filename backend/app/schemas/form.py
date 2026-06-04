from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime
from typing import List, Optional, Any

class FormFieldCreate(BaseModel):
    label: str
    helper_text: Optional[str] = None
    field_type: str
    is_required: bool = False
    options: Optional[List[Any]] = None
    sort_order: int

class FormFieldRead(BaseModel):
    id: uuid.UUID
    form_template_id: uuid.UUID
    label: str
    helper_text: Optional[str]
    field_type: str
    is_required: bool
    options: Optional[List[Any]]
    sort_order: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class FormTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None

class FormTemplateRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class FormSubmissionCreate(BaseModel):
    form_template_id: uuid.UUID
    title: str

class FormSubmissionRead(BaseModel):
    id: uuid.UUID
    form_template_id: uuid.UUID
    project_id: uuid.UUID
    client_id: uuid.UUID
    title: str
    status: str
    submitted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class FormResponseItem(BaseModel):
    field_id: uuid.UUID
    value_text: Optional[str] = None
    value_file_object_key: Optional[str] = None

class FormResponsePayload(BaseModel):
    responses: List[FormResponseItem]

class FormResponseRead(BaseModel):
    id: uuid.UUID
    form_submission_id: uuid.UUID
    form_field_id: uuid.UUID
    value_text: Optional[str]
    value_file_url: Optional[str]
    value_file_object_key: Optional[str]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PortalFormPayload(BaseModel):
    submission: FormSubmissionRead
    fields: List[FormFieldRead]
    responses: List[FormResponseRead]

class PresignedFormUrlRequest(BaseModel):
    filename: str
    content_type: str
