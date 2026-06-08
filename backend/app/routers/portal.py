from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
import datetime
from pydantic import BaseModel

from app.dependencies.db import get_db
from app.models.client_session import ClientSession
from app.models.project import Project
from app.schemas.project import ProjectRead
from app.models.deliverable import Deliverable
from app.schemas.deliverable import DeliverableRead
import uuid
from app.services.notifications_service import create_notification

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

from app.models.client import Client
from app.schemas.client import PortalMeResponse

@router.get("/me", response_model=PortalMeResponse, summary="Get current client profile")
async def get_portal_me(session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    if session.client_member_id:
        result = await db.execute(select(ClientMember).where(ClientMember.id == session.client_member_id))
        member = result.scalar_one_or_none()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        return {
            "id": member.id,
            "name": member.name,
            "email": member.email,
            "role": "member",
            "onboarding_dismissed_at": session.onboarding_dismissed_at
        }
    else:
        result = await db.execute(select(Client).where(Client.id == session.client_id))
        client = result.scalar_one_or_none()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "role": "primary",
            "avatar_url": client.avatar_url,
            "phone": client.phone,
            "address": client.address,
            "notification_email_prefs": client.notification_email_prefs,
            "onboarding_dismissed_at": session.onboarding_dismissed_at
        }

@router.post("/onboarding/dismiss", summary="Dismiss client onboarding")
async def dismiss_onboarding(session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    session.onboarding_dismissed_at = now
    await db.commit()
    return {"ok": True}

from app.schemas.client import NotificationPrefsUpdate

@router.patch("/me/notification-preferences", summary="Update notification preferences")
async def update_portal_notification_prefs(
    payload: NotificationPrefsUpdate,
    session: ClientSession = Depends(get_current_client_session),
    db: AsyncSession = Depends(get_db)
):
    if session.client_member_id:
        # Members do not have notification prefs in MVP
        raise HTTPException(status_code=403, detail="Only the primary client can update notification preferences.")
        
    result = await db.execute(select(Client).where(Client.id == session.client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
        
    client.notification_email_prefs = payload.prefs
    client.updated_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    await db.commit()
    return {"ok": True, "prefs": client.notification_email_prefs}

class AvatarUpdate(BaseModel):
    avatar_url: str

class PresignedUrlRequest(BaseModel):
    filename: str
    content_type: str

class PresignedUrlResponse(BaseModel):
    presigned_url: str
    object_key: str

@router.patch("/me/avatar", summary="Update avatar URL")
async def update_portal_avatar(
    payload: AvatarUpdate,
    session: ClientSession = Depends(get_current_client_session),
    db: AsyncSession = Depends(get_db)
):
    if session.client_member_id:
        raise HTTPException(status_code=403, detail="Only the primary client can update their avatar.")
        
    result = await db.execute(select(Client).where(Client.id == session.client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
        
    client.avatar_url = payload.avatar_url
    client.updated_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    await db.commit()
    return {"ok": True, "avatar_url": client.avatar_url}

@router.post("/me/avatar/presigned-url", summary="Get presigned URL for avatar upload")
async def generate_avatar_presigned_url(
    req: PresignedUrlRequest,
    session: ClientSession = Depends(get_current_client_session),
    db: AsyncSession = Depends(get_db)
):
    if session.client_member_id:
        raise HTTPException(status_code=403, detail="Only the primary client can upload an avatar.")

    s3 = boto3.client(
        's3',
        endpoint_url=f"https://{settings.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name="auto"
    )

    object_key = f"avatars/client_{session.client_id}/{uuid.uuid4()}_{req.filename}"

    try:
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': settings.R2_BUCKET_NAME,
                'Key': object_key,
                'ContentType': req.content_type
            },
            ExpiresIn=3600
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"presigned_url": url, "object_key": object_key}

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

from app.models.milestone import ProjectMilestone
from app.schemas.milestone import MilestoneRead

@router.get(
    "/projects/{project_id}/milestones",
    response_model=List[MilestoneRead],
    summary="List milestones for a client project"
)
async def list_portal_milestones(project_id: uuid.UUID, session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id, Project.client_id == session.client_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")
        
    result = await db.execute(
        select(ProjectMilestone)
        .where(ProjectMilestone.project_id == project_id)
        .order_by(ProjectMilestone.sort_order.asc(), ProjectMilestone.due_date.asc().nulls_last())
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
import boto3
from app.config import settings

import boto3
from app.config import settings

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
    background_tasks: BackgroundTasks,
    session: ClientSession = Depends(get_current_client_session),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(FormSubmission, Project.user_id)
        .join(Project, FormSubmission.project_id == Project.id)
        .where(FormSubmission.id == submission_id, FormSubmission.client_id == session.client_id)
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Form not found")
        
    sub, user_id = row

    # In a full app, we would loop through template.fields where is_required=True and verify a response exists.
    
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    sub.status = "completed"
    sub.submitted_at = now
    sub.updated_at = now
    
    await db.commit()
    
    await create_notification(
        db=db,
        background_tasks=background_tasks,
        recipient_type="user",
        recipient_id=user_id,
        notification_type="form_submitted",
        entity_type="form_submission",
        entity_id=sub.id,
        title="Form Submitted",
        message=f"A client completed the form: {sub.title}",
        link_url=f"/dashboard/projects/{sub.project_id}/forms/{sub.id}",
        project_id=sub.project_id
    )
    
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

from app.models.client_member import ClientMember
from app.schemas.client import ClientMemberCreate, ClientMemberRead

@router.get("/members", response_model=List[ClientMemberRead], summary="List team members")
async def list_portal_members(session: ClientSession = Depends(get_current_client_session), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ClientMember)
        .where(ClientMember.client_id == session.client_id)
        .order_by(ClientMember.created_at.asc())
    )
    return result.scalars().all()

@router.post("/members", response_model=ClientMemberRead, summary="Invite a team member")
async def create_portal_member(
    payload: ClientMemberCreate,
    session: ClientSession = Depends(get_current_client_session),
    db: AsyncSession = Depends(get_db)
):
    # Only primary client can invite (not other members)
    if session.client_member_id is not None:
        raise HTTPException(status_code=403, detail="Only the primary client can manage team members.")
        
    # Check limit of 3
    result = await db.execute(
        select(ClientMember)
        .where(ClientMember.client_id == session.client_id)
    )
    members = result.scalars().all()
    if len(members) >= 3:
        raise HTTPException(status_code=400, detail="Maximum of 3 team members reached.")
        
    # Check if email exists
    for m in members:
        if m.email.lower() == payload.email.lower():
            raise HTTPException(status_code=400, detail="A member with this email already exists.")
            
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    new_member = ClientMember(
        id=uuid.uuid4(),
        client_id=session.client_id,
        name=payload.name,
        email=payload.email,
        member_token=uuid.uuid4(),
        created_at=now
    )
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)
    
    # In a full production app, we would use Resend to email the unique `member_token` link here.
    return new_member

@router.delete("/members/{member_id}", summary="Remove a team member")
async def delete_portal_member(
    member_id: uuid.UUID,
    session: ClientSession = Depends(get_current_client_session),
    db: AsyncSession = Depends(get_db)
):
    if session.client_member_id is not None:
        raise HTTPException(status_code=403, detail="Only the primary client can manage team members.")
        
    result = await db.execute(
        select(ClientMember).where(ClientMember.id == member_id, ClientMember.client_id == session.client_id)
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found.")
        
    await db.delete(member)
    # Also invalidate their sessions
    await db.execute(
        ClientSession.__table__.delete().where(ClientSession.client_member_id == member_id)
    )
    await db.commit()
    
    return {"ok": True, "message": "Team member removed."}
