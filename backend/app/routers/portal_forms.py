from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
from datetime import datetime

from app.dependencies.db import get_db
from app.schemas.form import PortalFormPayload, FormResponsePayload, FormSubmissionRead, FormResponseRead, PresignedFormUrlRequest
from app.schemas.file_upload import PresignedUrlResponse
from app.models.client_session import ClientSession
from app.models.form_submission import FormSubmission
from app.models.form_field import FormField
from app.models.form_response import FormResponse
from app.services.s3_service import generate_presigned_put_url
from app.config import settings
from app.services.email_service import send_templated_email
from app.models.user import User
from app.models.client import Client

router = APIRouter(tags=["portal_forms"])

async def get_client_session(request: Request, db: AsyncSession):
    session_token = request.cookies.get("cp_session")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = await db.execute(select(ClientSession).where(ClientSession.session_token == session_token))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    return session

@router.get("/portal/forms/{submission_id}", response_model=PortalFormPayload)
async def get_portal_form(
    submission_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    session = await get_client_session(request, db)
    
    result = await db.execute(select(FormSubmission).where(FormSubmission.id == submission_id, FormSubmission.client_id == session.client_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Form not found")
        
    result = await db.execute(select(FormField).where(FormField.form_template_id == submission.form_template_id).order_by(FormField.sort_order.asc()))
    fields = result.scalars().all()
    
    result = await db.execute(select(FormResponse).where(FormResponse.form_submission_id == submission_id))
    responses = result.scalars().all()
    
    for r in responses:
        if r.value_file_object_key:
            r.value_file_url = f"{settings.R2_PUBLIC_URL}/{r.value_file_object_key}" if settings.R2_PUBLIC_URL else r.value_file_object_key

    return PortalFormPayload(
        submission=submission,
        fields=fields,
        responses=responses
    )

@router.post("/portal/forms/{submission_id}/responses")
async def save_form_responses(
    submission_id: uuid.UUID,
    payload: FormResponsePayload,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    session = await get_client_session(request, db)
    
    result = await db.execute(select(FormSubmission).where(FormSubmission.id == submission_id, FormSubmission.client_id == session.client_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Form not found")
        
    for r in payload.responses:
        result = await db.execute(select(FormResponse).where(FormResponse.form_submission_id == submission_id, FormResponse.form_field_id == r.field_id))
        existing_response = result.scalar_one_or_none()
        
        if existing_response:
            existing_response.value_text = r.value_text
            existing_response.value_file_object_key = r.value_file_object_key
        else:
            new_resp = FormResponse(
                form_submission_id=submission_id,
                form_field_id=r.field_id,
                value_text=r.value_text,
                value_file_object_key=r.value_file_object_key
            )
            db.add(new_resp)
            
    if submission.status == "pending":
        submission.status = "partial"
        
    await db.commit()
    return {"status": "saved"}

@router.post("/portal/forms/{submission_id}/submit")
async def submit_form(
    submission_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    session = await get_client_session(request, db)
    
    result = await db.execute(select(FormSubmission).where(FormSubmission.id == submission_id, FormSubmission.client_id == session.client_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Form not found")
        
    result = await db.execute(select(FormField).where(FormField.form_template_id == submission.form_template_id))
    fields = result.scalars().all()
    
    result = await db.execute(select(FormResponse).where(FormResponse.form_submission_id == submission_id))
    responses = result.scalars().all()
    response_map = {r.form_field_id: r for r in responses}
    
    for field in fields:
        if field.is_required:
            resp = response_map.get(field.id)
            if not resp or (not resp.value_text and not resp.value_file_object_key):
                raise HTTPException(status_code=400, detail=f"Field {field.label} is required")
                
    submission.status = "completed"
    submission.submitted_at = datetime.utcnow()
    await db.commit()
    
    result = await db.execute(select(Client).where(Client.id == session.client_id))
    client = result.scalar_one_or_none()
    
    result = await db.execute(select(User).where(User.id == client.user_id))
    user = result.scalar_one_or_none()
    
    send_templated_email(
        to_email=user.email,
        template_name="magic_link",
        context={"subject": "Client completed the form", "portal_url": "http://localhost:3000/dashboard"}
    )
    
    return {"status": "completed"}

@router.post("/portal/forms/{submission_id}/fields/{field_id}/presigned-url", response_model=PresignedUrlResponse)
async def generate_form_presigned_url(
    submission_id: uuid.UUID,
    field_id: uuid.UUID,
    payload: PresignedFormUrlRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    session = await get_client_session(request, db)
    
    result = await db.execute(select(FormSubmission).where(FormSubmission.id == submission_id, FormSubmission.client_id == session.client_id))
    submission = result.scalar_one_or_none()
    if not submission:
        raise HTTPException(status_code=404, detail="Form not found")
        
    object_key = f"forms/{submission_id}/{field_id}/{uuid.uuid4()}_{payload.filename}"
    url = generate_presigned_put_url(object_key, payload.content_type)
    
    return PresignedUrlResponse(
        presigned_url=url,
        object_key=object_key
    )
