from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

# --- Form Fields ---
class FormFieldBase(BaseModel):
    label: str
    helper_text: Optional[str] = None
    field_type: str # 'text', 'long_text', 'file_upload', 'multiple_choice'
    is_required: bool = False
    options: Optional[List[str]] = None
    sort_order: int

class FormFieldCreate(FormFieldBase):
    pass

class FormFieldRead(FormFieldBase):
    id: uuid.UUID
    form_template_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Form Templates ---
class FormTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None

class FormTemplateCreate(FormTemplateBase):
    pass

class FormTemplateRead(FormTemplateBase):
    id: uuid.UUID
    user_id: uuid.UUID
    fields: List[FormFieldRead] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Form Responses ---
class FormResponseBase(BaseModel):
    form_field_id: uuid.UUID
    value_text: Optional[str] = None
    value_file_url: Optional[str] = None
    value_file_object_key: Optional[str] = None

class FormResponseCreate(FormResponseBase):
    pass

class FormResponseRead(FormResponseBase):
    id: uuid.UUID
    form_submission_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Form Submissions ---
class FormSubmissionBase(BaseModel):
    form_template_id: uuid.UUID
    project_id: uuid.UUID
    title: str

class FormSubmissionCreate(FormSubmissionBase):
    pass

class FormSubmissionRead(FormSubmissionBase):
    id: uuid.UUID
    client_id: uuid.UUID
    status: str # 'pending', 'partial', 'completed'
    submitted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    responses: List[FormResponseRead] = []
    model_config = ConfigDict(from_attributes=True)
