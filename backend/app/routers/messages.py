from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user_optional
from app.schemas.message import MessageRead
from app.models.message import Message
from app.models.project import Project
from app.models.client_session import ClientSession
from app.models.user import User

router = APIRouter(tags=["messages"])

@router.get(
    "/projects/{project_id}/messages",
    response_model=List[MessageRead],
    summary="Get project messages"
)
async def get_messages(
    project_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    has_access = False
    
    if current_user:
        result = await db.execute(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
        if result.scalar_one_or_none():
            has_access = True
            
    if not has_access:
        session_token = request.cookies.get("cp_session")
        if session_token:
            result = await db.execute(select(ClientSession).where(ClientSession.session_token == session_token))
            session = result.scalar_one_or_none()
            if session:
                result = await db.execute(select(Project).where(Project.id == project_id, Project.client_id == session.client_id))
                if result.scalar_one_or_none():
                    has_access = True
                    
    if not has_access:
        raise HTTPException(status_code=403, detail="Not authorized to view messages for this project")

    result = await db.execute(
        select(Message)
        .where(Message.project_id == project_id)
        .order_by(Message.created_at.asc())
    )
    return result.scalars().all()
