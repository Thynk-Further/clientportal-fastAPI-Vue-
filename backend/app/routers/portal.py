from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
import datetime

from app.dependencies.db import get_db
from app.models.client_session import ClientSession
from app.models.project import Project
from app.schemas.project import ProjectRead
from app.models.deliverable import Deliverable
from app.schemas.deliverable import DeliverableRead
import uuid

router = APIRouter(tags=["portal"])

async def get_current_client_session(request: Request, db: AsyncSession = Depends(get_db)):
    session_token = request.cookies.get("cp_session")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated. Missing cp_session cookie.")
        
    result = await db.execute(
        select(ClientSession)
        .where(ClientSession.session_token == session_token)
    )
    client_session = result.scalar_one_or_none()
    
    if not client_session or client_session.expires_at < datetime.datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session expired or invalid. Please request a new magic link.")
        
    return client_session

@router.get(
    "/projects",
    response_model=List[ProjectRead],
    summary="List client projects",
    description="Returns all projects assigned to the authenticated client."
)
async def list_portal_projects(session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Project)
        .where(Project.client_id == session.client_id)
        .order_by(Project.created_at.desc())
    )
    return result.scalars().all()

@router.get(
    "/projects/{project_id}",
    response_model=ProjectRead,
    summary="Get client project",
    description="Returns a specific project if assigned to the client."
)
async def get_portal_project(project_id: uuid.UUID, session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id, Project.client_id == session.client_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get(
    "/projects/{project_id}/deliverables",
    response_model=List[DeliverableRead],
    summary="List deliverables for a client project"
)
async def list_portal_deliverables(project_id: uuid.UUID, session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    # First verify they have access to the project
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id, Project.client_id == session.client_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")
        
    result = await db.execute(
        select(Deliverable)
        .options(selectinload(Deliverable.file_uploads))
        .where(Deliverable.project_id == project_id)
        .order_by(Deliverable.created_at.asc())
    )
    return result.scalars().all()

from app.models.message import Message
from app.schemas.message import MessageRead

@router.get(
    "/projects/{project_id}/messages",
    response_model=List[MessageRead],
    summary="Get project messages for client"
)
async def get_portal_messages(project_id: uuid.UUID, session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    # Verify access
    result = await db.execute(select(Project).where(Project.id == project_id, Project.client_id == session.client_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(
        select(Message)
        .where(Message.project_id == project_id)
        .order_by(Message.created_at.asc())
    )
    return result.scalars().all()

from app.models.form_submission import FormSubmission
from app.models.form_template import FormTemplate
from app.models.form_response import FormResponse
from app.schemas.form import FormSubmissionRead, FormResponseRead, FormResponseCreate
from pydantic import BaseModel
import boto3
from app.config import settings

class PresignedUrlRequest(BaseModel):
    filename: str
    content_type: str

class PresignedUrlResponse(BaseModel):
    presigned_url: str
    object_key: str

@router.get("/forms", response_model=List[FormSubmissionRead], summary="List client form assignments")
async def list_portal_forms(session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FormSubmission)
        .options(selectinload(FormSubmission.responses))
        .where(FormSubmission.client_id == session.client_id)
        .order_by(FormSubmission.created_at.desc())
    )
    return result.scalars().all()

@router.get("/forms/{submission_id}")
async def get_portal_form(submission_id: uuid.UUID, session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    # Get submission
    result = await db.execute(
        select(FormSubmission)
        .options(selectinload(FormSubmission.responses))
        .where(FormSubmission.id == submission_id, FormSubmission.client_id == session.client_id)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Form not found")

    # Get template and fields
    template_res = await db.execute(
        select(FormTemplate)
        .options(selectinload(FormTemplate.fields))
        .where(FormTemplate.id == sub.form_template_id)
    )
    template = template_res.scalar_one_or_none()
    
    # Sort fields
    template.fields.sort(key=lambda x: x.sort_order)

    return {
        "submission": sub,
        "template": template
    }

class BulkResponsesCreate(BaseModel):
    responses: List[FormResponseCreate]

@router.post("/forms/{submission_id}/responses")
async def save_form_responses(
    submission_id: uuid.UUID,
    payload: BulkResponsesCreate,
    session: ClientSession = Depends(get_current_client_session),
    db: AsyncSession = Depends(get_db)
):
    # Verify access
    result = await db.execute(select(FormSubmission).where(FormSubmission.id == submission_id, FormSubmission.client_id == session.client_id))
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Form not found")
        
    if sub.status == "completed":
        raise HTTPException(status_code=400, detail="Form is already submitted")

    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

    for resp_in in payload.responses:
        # Check if exists
        exist_res = await db.execute(select(FormResponse).where(
            FormResponse.form_submission_id == submission_id,
            FormResponse.form_field_id == resp_in.form_field_id
        ))
        existing = exist_res.scalar_one_or_none()

        if existing:
            existing.value_text = resp_in.value_text
            existing.value_file_object_key = resp_in.value_file_object_key
            existing.updated_at = now
        else:
            new_resp = FormResponse(
                id=uuid.uuid4(),
                form_submission_id=submission_id,
                form_field_id=resp_in.form_field_id,
                value_text=resp_in.value_text,
                value_file_object_key=resp_in.value_file_object_key,
                created_at=now,
                updated_at=now
            )
            db.add(new_resp)
            
    # Mark as partial
    sub.status = "partial"
    sub.updated_at = now
    
    await db.commit()
    return {"ok": True, "status": "partial"}

@router.post("/forms/{submission_id}/submit")
async def complete_form_submission(
    submission_id: uuid.UUID,
    session: ClientSession = Depends(get_current_client_session),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(FormSubmission).where(FormSubmission.id == submission_id, FormSubmission.client_id == session.client_id))
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Form not found")

    # In a full app, we would loop through template.fields where is_required=True and verify a response exists.
    
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    sub.status = "completed"
    sub.submitted_at = now
    sub.updated_at = now
    
    await db.commit()
    return {"ok": True, "status": "completed"}

@router.post("/forms/{submission_id}/fields/{field_id}/presigned-url", response_model=PresignedUrlResponse)
async def generate_form_presigned_url(
    submission_id: uuid.UUID,
    field_id: uuid.UUID,
    req: PresignedUrlRequest,
    session: ClientSession = Depends(get_current_client_session),
    db: AsyncSession = Depends(get_db)
):
    # Verify access
    result = await db.execute(select(FormSubmission).where(FormSubmission.id == submission_id, FormSubmission.client_id == session.client_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Form not found")

    s3 = boto3.client(
        's3',
        endpoint_url=f"https://{settings.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name="auto"
    )

    object_key = f"forms/{submission_id}/{field_id}/{uuid.uuid4()}_{req.filename}"

    try:
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': settings.R2_BUCKET_NAME,
                'Key': object_key,
                'ContentType': req.content_type
            },
            ExpiresIn=3600 # 1 hour
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"presigned_url": url, "object_key": object_key}
