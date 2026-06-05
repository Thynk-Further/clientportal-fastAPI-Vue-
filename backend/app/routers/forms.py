from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import desc
from typing import List
import uuid
from datetime import datetime, timezone

from app.dependencies.db import get_db
from app.models.form_template import FormTemplate
from app.models.form_field import FormField
from app.models.form_submission import FormSubmission
from app.models.project import Project
from app.models.client import Client
from app.schemas.form import (
    FormTemplateRead, FormTemplateCreate, FormFieldCreate, FormFieldRead,
    FormSubmissionRead, FormSubmissionCreate
)
from app.routers.auth import get_current_user
from app.schemas.user import UserRead

router = APIRouter(tags=["Forms"])

# --- FORM TEMPLATES ---

@router.get("/form-templates", response_model=List[FormTemplateRead])
async def list_form_templates(
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    result = await db.execute(
        select(FormTemplate)
        .options(selectinload(FormTemplate.fields))
        .filter(FormTemplate.user_id == current_user.id)
        .order_by(desc(FormTemplate.created_at))
    )
    return result.scalars().all()

@router.post("/form-templates", response_model=FormTemplateRead)
async def create_form_template(
    template_in: FormTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    db_template = FormTemplate(
        id=uuid.uuid4(),
        user_id=current_user.id,
        name=template_in.name,
        description=template_in.description,
        created_at=now,
        updated_at=now
    )
    db.add(db_template)
    await db.commit()
    await db.refresh(db_template)
    # Return with empty fields list for the schema
    db_template.fields = []
    return db_template

@router.get("/form-templates/{template_id}", response_model=FormTemplateRead)
async def get_form_template(
    template_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    result = await db.execute(
        select(FormTemplate)
        .options(selectinload(FormTemplate.fields))
        .filter(FormTemplate.id == template_id, FormTemplate.user_id == current_user.id)
    )
    template = result.scalars().first()
    if not template:
        raise HTTPException(status_code=404, detail="Form template not found")
    
    # Ensure fields are sorted by sort_order
    template.fields.sort(key=lambda x: x.sort_order)
    return template

@router.post("/form-templates/{template_id}/fields", response_model=List[FormFieldRead])
async def update_template_fields(
    template_id: uuid.UUID,
    fields_in: List[FormFieldCreate],
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    # Verify ownership
    result = await db.execute(select(FormTemplate).filter(FormTemplate.id == template_id, FormTemplate.user_id == current_user.id))
    template = result.scalars().first()
    if not template:
        raise HTTPException(status_code=404, detail="Form template not found")

    # Delete existing fields
    existing_fields = await db.execute(select(FormField).filter(FormField.form_template_id == template_id))
    for field in existing_fields.scalars().all():
        await db.delete(field)
    
    # Add new fields
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    new_fields = []
    for field_in in fields_in:
        db_field = FormField(
            id=uuid.uuid4(),
            form_template_id=template_id,
            label=field_in.label,
            helper_text=field_in.helper_text,
            field_type=field_in.field_type,
            is_required=field_in.is_required,
            options=field_in.options,
            sort_order=field_in.sort_order,
            created_at=now
        )
        db.add(db_field)
        new_fields.append(db_field)
    
    template.updated_at = now
    await db.commit()
    
    for f in new_fields:
        await db.refresh(f)
    
    return new_fields

# --- FORM SUBMISSIONS (ASSIGNMENTS) ---

@router.get("/form-submissions", response_model=List[FormSubmissionRead])
async def list_form_submissions(
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    # Fetch all form submissions for projects owned by the freelancer
    # We do a join on Project to ensure ownership
    result = await db.execute(
        select(FormSubmission)
        .join(Project, Project.id == FormSubmission.project_id)
        .filter(Project.user_id == current_user.id)
        .options(selectinload(FormSubmission.responses))
        .order_by(desc(FormSubmission.created_at))
    )
    return result.scalars().all()

@router.post("/projects/{project_id}/forms", response_model=FormSubmissionRead)
async def assign_form_to_project(
    project_id: uuid.UUID,
    sub_in: FormSubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    # Verify project
    project_res = await db.execute(select(Project).filter(Project.id == project_id, Project.user_id == current_user.id))
    project = project_res.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Verify template exists
    template_res = await db.execute(select(FormTemplate).filter(FormTemplate.id == sub_in.form_template_id, FormTemplate.user_id == current_user.id))
    template = template_res.scalars().first()
    if not template:
        raise HTTPException(status_code=404, detail="Form template not found")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    db_submission = FormSubmission(
        id=uuid.uuid4(),
        form_template_id=sub_in.form_template_id,
        project_id=project_id,
        client_id=project.client_id,
        title=sub_in.title,
        status="pending",
        created_at=now,
        updated_at=now
    )
    
    db.add(db_submission)
    await db.commit()
    await db.refresh(db_submission)
    
    db_submission.responses = []
    
    # TODO: In a full production app, dispatch Resend email here: "You have a new form to complete in the portal!"
    
    return db_submission
