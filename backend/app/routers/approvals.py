from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.schemas.approval import ApprovalCreate, ApprovalRead
from app.models.user import User
from app.models.client import Client
from app.models.client_session import ClientSession
from app.models.project import Project
from app.models.deliverable import Deliverable
from app.models.approval import Approval
from app.services.pdf_service import generate_approval_history_pdf

router = APIRouter(tags=["approvals"])

async def get_client_from_session(request: Request, db: AsyncSession):
    session_token = request.cookies.get("cp_session")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated as client")
        
    result = await db.execute(
        select(ClientSession)
        .where(ClientSession.session_token == session_token)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
        
    result = await db.execute(select(Client).where(Client.id == session.client_id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=401, detail="Client not found")
        
    return client

@router.post(
    "/portal/approvals/{deliverable_id}",
    response_model=ApprovalRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create an approval (Client Portal)"
)
async def create_approval(
    deliverable_id: uuid.UUID,
    approval_data: ApprovalCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    client = await get_client_from_session(request, db)
    
    result = await db.execute(
        select(Deliverable)
        .join(Project, Deliverable.project_id == Project.id)
        .where(Deliverable.id == deliverable_id, Project.client_id == client.id)
    )
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    client_ip = request.client.host if request.client else None
    client_user_agent = request.headers.get("user-agent")

    approval = Approval(
        deliverable_id=deliverable_id,
        client_id=client.id,
        action=approval_data.action,
        comment=approval_data.comment,
        client_ip=client_ip,
        client_user_agent=client_user_agent
    )
    db.add(approval)
    
    if approval_data.action == "approved":
        deliverable.status = "approved"
    
    await db.commit()
    await db.refresh(approval)
    
    return approval

@router.get(
    "/deliverables/{deliverable_id}/approvals/export",
    summary="Export approval history as PDF"
)
async def export_approvals(
    deliverable_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Deliverable)
        .join(Project, Deliverable.project_id == Project.id)
        .where(Deliverable.id == deliverable_id, Project.user_id == current_user.id)
    )
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    result = await db.execute(
        select(Approval)
        .where(Approval.deliverable_id == deliverable_id)
        .order_by(Approval.created_at.asc())
    )
    approvals = result.scalars().all()

    pdf_buffer = generate_approval_history_pdf(approvals, deliverable.name)
    
    headers = {
        'Content-Disposition': f'attachment; filename="approval_history_{deliverable.name}.pdf"'
    }
    
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)
