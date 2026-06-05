from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List
import uuid
from datetime import datetime, timezone

from app.database import get_db
from app.models.time_entry import TimeEntry
from app.models.project import Project
from app.schemas.time_entry import TimeEntryRead, TimeEntryCreate, TimeEntryManualCreate, TimeEntryUpdate
from app.routers.auth import get_current_user
from app.schemas.user import UserRead

router = APIRouter(tags=["Time Entries"])

@router.get("/projects/{project_id}/time-entries", response_model=List[TimeEntryRead])
async def list_time_entries(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    # Verify project ownership
    result = await db.execute(select(Project).filter(Project.id == project_id, Project.user_id == current_user.id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(
        select(TimeEntry)
        .filter(TimeEntry.project_id == project_id)
        .order_by(desc(TimeEntry.started_at))
    )
    return result.scalars().all()

@router.post("/projects/{project_id}/time-entries/start", response_model=TimeEntryRead)
async def start_timer(
    project_id: uuid.UUID,
    entry_in: TimeEntryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    # Verify project ownership
    result = await db.execute(select(Project).filter(Project.id == project_id, Project.user_id == current_user.id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check for active timer
    active_result = await db.execute(
        select(TimeEntry)
        .filter(TimeEntry.user_id == current_user.id, TimeEntry.ended_at.is_(None))
    )
    active_entry = active_result.scalars().first()
    if active_entry:
        raise HTTPException(status_code=409, detail="A timer is already running")

    now = datetime.now(timezone.utc)
    started_at = entry_in.started_at or now

    hourly_rate = entry_in.hourly_rate_cents or project.default_hourly_rate_cents or current_user.default_hourly_rate_cents

    db_entry = TimeEntry(
        id=uuid.uuid4(),
        project_id=project_id,
        deliverable_id=entry_in.deliverable_id,
        user_id=current_user.id,
        description=entry_in.description,
        started_at=started_at.replace(tzinfo=None), # SQLite naive compat
        is_billable=entry_in.is_billable,
        hourly_rate_cents=hourly_rate,
        created_at=now.replace(tzinfo=None),
        updated_at=now.replace(tzinfo=None)
    )
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

@router.post("/time-entries/{entry_id}/stop", response_model=TimeEntryRead)
async def stop_timer(
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    result = await db.execute(select(TimeEntry).filter(TimeEntry.id == entry_id, TimeEntry.user_id == current_user.id))
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Time entry not found")
    
    if entry.ended_at is not None:
        raise HTTPException(status_code=400, detail="Timer is already stopped")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    entry.ended_at = now
    
    # Calculate duration
    duration = (entry.ended_at - entry.started_at).total_seconds()
    entry.duration_seconds = int(duration)
    entry.updated_at = now

    await db.commit()
    await db.refresh(entry)
    return entry

@router.post("/projects/{project_id}/time-entries/manual", response_model=TimeEntryRead)
async def create_manual_entry(
    project_id: uuid.UUID,
    entry_in: TimeEntryManualCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    # Verify project
    result = await db.execute(select(Project).filter(Project.id == project_id, Project.user_id == current_user.id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if entry_in.ended_at <= entry_in.started_at:
        raise HTTPException(status_code=400, detail="ended_at must be after started_at")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    
    # Ensure timezone unaware for sqlite compat
    started = entry_in.started_at.replace(tzinfo=None)
    ended = entry_in.ended_at.replace(tzinfo=None)
    
    duration = (ended - started).total_seconds()
    hourly_rate = entry_in.hourly_rate_cents or project.default_hourly_rate_cents or current_user.default_hourly_rate_cents

    db_entry = TimeEntry(
        id=uuid.uuid4(),
        project_id=project_id,
        deliverable_id=entry_in.deliverable_id,
        user_id=current_user.id,
        description=entry_in.description,
        started_at=started,
        ended_at=ended,
        duration_seconds=int(duration),
        is_billable=entry_in.is_billable,
        hourly_rate_cents=hourly_rate,
        created_at=now,
        updated_at=now
    )
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry

@router.delete("/time-entries/{entry_id}")
async def delete_time_entry(
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    result = await db.execute(select(TimeEntry).filter(TimeEntry.id == entry_id, TimeEntry.user_id == current_user.id))
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Time entry not found")
        
    if entry.invoice_id:
        raise HTTPException(status_code=400, detail="Cannot delete a time entry that has been invoiced")

    await db.delete(entry)
    await db.commit()
    return {"ok": True}
