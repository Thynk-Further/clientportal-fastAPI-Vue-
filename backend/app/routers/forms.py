from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.schemas.form import FormTemplateCreate, FormTemplateRead, FormFieldCreate, FormFieldRead, FormSubmissionCreate, FormSubmissionRead
from app.models.user import User
from app.models.project import Project
from app.models.client import Client
from app.models.form_template import FormTemplate
from app.models.form_field import FormField
from app.models.form_submission import FormSubmission
from app.services.email_service import send_templated_email

router = APIRouter(tags=["forms"])

@router.post("/form-templates", response_model=FormTemplateRead, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: FormTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    template = FormTemplate(
        user_id=current_user.id,
        name=template_data.name,
        description=template_data.description
    )
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template

@router.get("/form-templates", response_model=List[FormTemplateRead])
async def list_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(FormTemplate).where(FormTemplate.user_id == current_user.id))
    return result.scalars().all()

@router.post("/form-templates/{template_id}/fields", response_model=List[FormFieldRead], status_code=status.HTTP_201_CREATED)
async def create_fields(
    template_id: uuid.UUID,
    fields_data: List[FormFieldCreate],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(FormTemplate).where(FormTemplate.id == template_id, FormTemplate.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Template not found")
        
    new_fields = []
    for f in fields_data:
        field = FormField(
            form_template_id=template_id,
            label=f.label,
            helper_text=f.helper_text,
            field_type=f.field_type,
            is_required=f.is_required,
            options=f.options,
            sort_order=f.sort_order
        )
        db.add(field)
        new_fields.append(field)
        
    await db.commit()
    for field in new_fields:
        await db.refresh(field)
        
    return new_fields

@router.post("/projects/{project_id}/forms", response_model=FormSubmissionRead, status_code=status.HTTP_201_CREATED)
async def assign_form(
    project_id: uuid.UUID,
    assignment_data: FormSubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    result = await db.execute(select(FormTemplate).where(FormTemplate.id == assignment_data.form_template_id, FormTemplate.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Template not found")
        
    result = await db.execute(select(Client).where(Client.id == project.client_id))
    client = result.scalar_one_or_none()
    
    submission = FormSubmission(
        form_template_id=assignment_data.form_template_id,
        project_id=project.id,
        client_id=project.client_id,
        title=assignment_data.title,
        status="pending"
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    
    send_templated_email(
        to_email=client.email,
        template_name="magic_link",
        context={"subject": "You have a new form to complete", "portal_url": f"http://localhost:3000/portal/{client.portal_token}"}
    )
    
    return submission
