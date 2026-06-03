from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.schemas.deliverable import DeliverableCreate, DeliverableUpdate, DeliverableRead
from app.models.user import User
from app.models.project import Project
from app.models.deliverable import Deliverable

router = APIRouter(tags=["deliverables"])

@router.get(
    "/projects/{project_id}/deliverables",
    response_model=List[DeliverableRead],
    summary="List deliverables for a project"
)
async def list_deliverables(project_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(select(Deliverable).where(Deliverable.project_id == project_id).order_by(Deliverable.created_at.asc()))
    return result.scalars().all()

@router.post(
    "/projects/{project_id}/deliverables",
    response_model=DeliverableRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a deliverable"
)
async def create_deliverable(
    project_id: uuid.UUID,
    deliverable_data: DeliverableCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")

    deliverable = Deliverable(
        project_id=project_id,
        name=deliverable_data.name,
        description=deliverable_data.description
    )
    db.add(deliverable)
    await db.commit()
    await db.refresh(deliverable)

    return deliverable

@router.get(
    "/deliverables/{deliverable_id}",
    response_model=DeliverableRead,
    summary="Get deliverable details"
)
async def get_deliverable(deliverable_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Deliverable)
        .join(Project, Deliverable.project_id == Project.id)
        .where(Deliverable.id == deliverable_id, Project.user_id == current_user.id)
    )
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")
    return deliverable

@router.patch(
    "/deliverables/{deliverable_id}",
    response_model=DeliverableRead,
    summary="Update deliverable"
)
async def update_deliverable(
    deliverable_id: uuid.UUID,
    update_data: DeliverableUpdate,
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

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(deliverable, key, value)

    await db.commit()
    await db.refresh(deliverable)
    
    return deliverable

@router.delete(
    "/deliverables/{deliverable_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete deliverable"
)
async def delete_deliverable(deliverable_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Deliverable)
        .join(Project, Deliverable.project_id == Project.id)
        .where(Deliverable.id == deliverable_id, Project.user_id == current_user.id)
    )
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    await db.execute(delete(Deliverable).where(Deliverable.id == deliverable_id))
    await db.commit()
    return None
