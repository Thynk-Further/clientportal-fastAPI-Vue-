from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import datetime

from app.dependencies.db import get_db
from app.models.client_session import ClientSession
from app.models.project import Project
from app.schemas.project import ProjectRead

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
