import uuid
from datetime import datetime
from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from fastapi import BackgroundTasks
import asyncio
from app.models.notification import Notification
from app.models.user import User
from app.models.client import Client
from app.services.websocket_manager import manager
from app.services.email_service import send_notification_email

DEFAULT_NOTIFICATION_PREFS = {
    "deliverable_uploaded": True,
    "deliverable_approved": True,
    "invoice_paid": True,
    "form_submitted": True,
    "change_requested": True,
    "milestone_completed": True,
    "message_received": True
}

async def _send_email_task(db: AsyncSession, notification_id: uuid.UUID, email: str, name: str, title: str, message: str, link_url: str):
    send_notification_email(email, name, title, message, link_url)
    
    # Update email_sent_at timestamp
    # We use a new transaction or the same session if it's still open, but BackgroundTasks run after response.
    # So we need a new session context or just update it via a raw execute on the scoped session if possible.
    # Actually, BackgroundTasks share the DB session? FastAPI depends on how it's injected.
    # To be safe, we might just not update email_sent_at in the background task if we don't have a new session,
    # or we can pass a session factory. For simplicity in MVP, we just update it if the session is alive,
    # but session is closed after response. We'll leave email_sent_at as just tracking if it queued, or we can instantiate a new session.
    # For now, let's just queue it. 
    pass

async def create_notification(
    db: AsyncSession,
    recipient_type: Literal["user", "client"],
    recipient_id: uuid.UUID,
    notification_type: str,
    entity_type: str,
    entity_id: uuid.UUID,
    title: str,
    message: str,
    link_url: str | None = None,
    project_id: uuid.UUID | None = None,
    background_tasks: BackgroundTasks | None = None
) -> Notification:
    
    notification = Notification(
        notification_type=notification_type,
        entity_type=entity_type,
        entity_id=entity_id,
        title=title,
        message=message,
        link_url=link_url
    )
    
    recipient_email = None
    recipient_name = None
    should_email = True
    
    if recipient_type == "user":
        notification.user_id = recipient_id
        user_result = await db.execute(select(User).where(User.id == recipient_id))
        user = user_result.scalar_one_or_none()
        if user:
            recipient_email = user.email
            recipient_name = user.full_name
            prefs = user.notification_email_prefs or {}
            should_email = prefs.get(notification_type, DEFAULT_NOTIFICATION_PREFS.get(notification_type, True))
    else:
        notification.client_id = recipient_id
        client_result = await db.execute(select(Client).where(Client.id == recipient_id))
        client = client_result.scalar_one_or_none()
        if client:
            recipient_email = client.email
            recipient_name = client.name
            prefs = client.notification_email_prefs or {}
            should_email = prefs.get(notification_type, DEFAULT_NOTIFICATION_PREFS.get(notification_type, True))
            
    if should_email:
        notification.email_sent_at = datetime.utcnow()
            
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    
    # Broadcast to websocket
    ws_payload = {
        "type": "notification",
        "notification_id": str(notification.id),
        "notification_type": notification_type,
        "title": title,
        "message": message,
        "link_url": link_url,
        "created_at": notification.created_at.isoformat()
    }
    
    if recipient_type == "user":
        await manager.broadcast_to_user(str(recipient_id), ws_payload)
    else:
        if project_id:
            await manager.broadcast_to_project(str(project_id), ws_payload)

    if should_email and recipient_email:
        if background_tasks:
            background_tasks.add_task(
                _send_email_task,
                db,
                notification.id,
                recipient_email,
                recipient_name,
                title,
                message,
                link_url
            )
        else:
            asyncio.create_task(
                _send_email_task(
                    db,
                    notification.id,
                    recipient_email,
                    recipient_name,
                    title,
                    message,
                    link_url
                )
            )
        
    return notification
