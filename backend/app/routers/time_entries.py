from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
from datetime import datetime

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.schemas.time_entry import TimeEntryStart, TimeEntryManual, TimeEntryRead
from app.models.user import User
from app.models.project import Project
from app.models.time_entry import TimeEntry

router = APIRouter(tags=["time_entries"])

@router.get(
    "/projects/{project_id}/time-entries",
    response_model=List[TimeEntryRead],
    summary="List all time entries for a project"
)
async def list_time_entries(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(
        select(TimeEntry).where(TimeEntry.project_id == project_id).order_by(TimeEntry.started_at.desc())
    )
    return result.scalars().all()

@router.post(
    "/projects/{project_id}/time-entries/start",
    response_model=TimeEntryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Start a live timer"
)
async def start_timer(
    project_id: uuid.UUID,
    entry_data: TimeEntryStart,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if entry_data.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project ID mismatch")

    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(
        select(TimeEntry).where(TimeEntry.user_id == current_user.id, TimeEntry.ended_at.is_(None))
    )
    active_timer = result.scalar_one_or_none()
    if active_timer:
        raise HTTPException(status_code=409, detail="TIMER_ALREADY_RUNNING")

    rate = project.default_hourly_rate_cents or current_user.default_hourly_rate_cents

    new_entry = TimeEntry(
        project_id=project.id,
        deliverable_id=entry_data.deliverable_id,
        user_id=current_user.id,
        description=entry_data.description,
        started_at=datetime.utcnow(),
        is_billable=entry_data.is_billable,
        hourly_rate_cents=rate
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)

    return new_entry

@router.post(
    "/time-entries/{entry_id}/stop",
    response_model=TimeEntryRead,
    summary="Stop a live timer"
)
async def stop_timer(
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(TimeEntry).where(TimeEntry.id == entry_id, TimeEntry.user_id == current_user.id)
    )
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Time entry not found")
        
    if entry.ended_at:
        raise HTTPException(status_code=400, detail="Timer already stopped")

    now = datetime.utcnow()
    entry.ended_at = now
    duration = now - entry.started_at
    entry.duration_seconds = int(duration.total_seconds())

    await db.commit()
    await db.refresh(entry)

    return entry

@router.post(
    "/projects/{project_id}/time-entries/manual",
    response_model=TimeEntryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a manual time entry"
)
async def create_manual_entry(
    project_id: uuid.UUID,
    entry_data: TimeEntryManual,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if entry_data.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project ID mismatch")

    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if entry_data.ended_at <= entry_data.started_at:
        raise HTTPException(status_code=400, detail="ended_at must be after started_at")

    duration = entry_data.ended_at - entry_data.started_at
    rate = project.default_hourly_rate_cents or current_user.default_hourly_rate_cents

    new_entry = TimeEntry(
        project_id=project.id,
        deliverable_id=entry_data.deliverable_id,
        user_id=current_user.id,
        description=entry_data.description,
        started_at=entry_data.started_at,
        ended_at=entry_data.ended_at,
        duration_seconds=int(duration.total_seconds()),
        is_billable=entry_data.is_billable,
        hourly_rate_cents=rate
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)

    return new_entry
