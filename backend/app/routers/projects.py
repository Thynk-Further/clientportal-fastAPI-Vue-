from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.models.user import User
from app.models.client import Client
from app.models.project import Project

router = APIRouter(tags=["projects"])

@router.get(
    "",
    response_model=List[ProjectRead],
    summary="List projects",
    description="List all projects owned by the authenticated freelancer."
)
async def list_projects(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Project).where(Project.user_id == current_user.id).order_by(Project.created_at.desc()))
    return result.scalars().all()

@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
    description="Creates a new project for a specific client."
)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Client).where(Client.id == project_data.client_id, Client.user_id == current_user.id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    project = Project(
        user_id=current_user.id,
        client_id=client.id,
        name=project_data.name,
        description=project_data.description,
        default_hourly_rate_cents=project_data.default_hourly_rate_cents
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)

    return project

@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Get project details"
)
async def get_project(project_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.patch(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Update project"
)
async def update_project(
    project_id: uuid.UUID,
    update_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    
    return project
