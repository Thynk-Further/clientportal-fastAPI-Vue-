from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import List
import uuid
import datetime

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import NotificationRead, NotificationListResponse

router = APIRouter(tags=["notifications"])

@router.get(
    "",
    response_model=NotificationListResponse,
    summary="List freelancer notifications"
)
async def list_notifications(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    unread_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Notification).where(Notification.user_id == current_user.id)
    if unread_only:
        query = query.where(Notification.read_at.is_(None))
        
    # Count unread
    count_query = select(func.count(Notification.id)).where(
        Notification.user_id == current_user.id,
        Notification.read_at.is_(None)
    )
    unread_count_res = await db.execute(count_query)
    unread_count = unread_count_res.scalar_one()

    # Get items
    query = query.order_by(Notification.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return {
        "items": items,
        "unread_count": unread_count
    }

@router.post(
    "/{notification_id}/read",
    summary="Mark notification as read"
)
async def mark_read(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Notification).where(Notification.id == notification_id, Notification.user_id == current_user.id))
    notification = result.scalar_one_or_none()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    if not notification.read_at:
        notification.read_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        await db.commit()
        
    return {"ok": True}

@router.post(
    "/read-all",
    summary="Mark all notifications as read"
)
async def mark_all_read(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    await db.execute(
        update(Notification)
        .where(Notification.user_id == current_user.id, Notification.read_at.is_(None))
        .values(read_at=now)
    )
    await db.commit()
    return {"ok": True}
