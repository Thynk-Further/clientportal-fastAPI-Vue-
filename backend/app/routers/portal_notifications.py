from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import List
import uuid
import datetime

from app.dependencies.db import get_db
from app.routers.portal import get_current_client_session
from app.models.client_session import ClientSession
from app.models.notification import Notification
from app.schemas.notification import NotificationRead, NotificationListResponse

router = APIRouter(tags=["portal_notifications"])

@router.get(
    "",
    response_model=NotificationListResponse,
    summary="List client notifications"
)
async def list_portal_notifications(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    unread_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    session: ClientSession = Depends(get_current_client_session)
):
    query = select(Notification).where(Notification.client_id == session.client_id)
    if unread_only:
        query = query.where(Notification.read_at.is_(None))
        
    count_query = select(func.count(Notification.id)).where(
        Notification.client_id == session.client_id,
        Notification.read_at.is_(None)
    )
    unread_count_res = await db.execute(count_query)
    unread_count = unread_count_res.scalar_one()

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
async def mark_portal_read(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    session: ClientSession = Depends(get_current_client_session)
):
    result = await db.execute(select(Notification).where(Notification.id == notification_id, Notification.client_id == session.client_id))
    notification = result.scalar_one_or_none()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    if not notification.read_at:
        notification.read_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        await db.commit()
        
    return {"ok": True}

@router.post(
    "/read-all",
    summary="Mark all portal notifications as read"
)
async def mark_all_portal_read(
    db: AsyncSession = Depends(get_db),
    session: ClientSession = Depends(get_current_client_session)
):
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    await db.execute(
        update(Notification)
        .where(Notification.client_id == session.client_id, Notification.read_at.is_(None))
        .values(read_at=now)
    )
    await db.commit()
    return {"ok": True}
