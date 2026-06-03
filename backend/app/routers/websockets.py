from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import uuid
import json

from app.dependencies.db import get_db
from app.services.websocket_manager import manager
from app.models.message import Message
from app.models.project import Project
from app.models.client_session import ClientSession
from app.models.user import User
from app.services.auth_service import decode_access_token

router = APIRouter(tags=["websockets"])

async def authenticate_ws(token: str, project_id: uuid.UUID, db: AsyncSession):
    if not token:
        return None, None, None

    result = await db.execute(select(ClientSession).where(ClientSession.session_token == token))
    session = result.scalar_one_or_none()
    
    if session:
        result = await db.execute(select(Project).where(Project.id == project_id, Project.client_id == session.client_id))
        project = result.scalar_one_or_none()
        if project:
            return "client", None, session.client_id
            
    payload = decode_access_token(token)
    if payload and payload.get("sub"):
        try:
            user_id = uuid.UUID(payload.get("sub"))
            result = await db.execute(select(Project).where(Project.id == project_id, Project.user_id == user_id))
            project = result.scalar_one_or_none()
            if project:
                return "freelancer", user_id, None
        except ValueError:
            pass

    return None, None, None

@router.websocket("/api/v1/ws/projects/{project_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    project_id: uuid.UUID,
    token: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    sender_type, sender_user_id, sender_client_id = await authenticate_ws(token, project_id, db)
    
    if not sender_type:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, project_id)
    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                payload = json.loads(data)
                content = payload.get("content")
                deliverable_id_str = payload.get("deliverable_id")
                deliverable_id = uuid.UUID(deliverable_id_str) if deliverable_id_str else None
                
                if content:
                    new_msg = Message(
                        project_id=project_id,
                        deliverable_id=deliverable_id,
                        sender_type=sender_type,
                        sender_user_id=sender_user_id,
                        sender_client_id=sender_client_id,
                        content=content
                    )
                    db.add(new_msg)
                    await db.commit()
                    await db.refresh(new_msg)
                    
                    msg_dict = {
                        "id": str(new_msg.id),
                        "project_id": str(new_msg.project_id),
                        "deliverable_id": str(new_msg.deliverable_id) if new_msg.deliverable_id else None,
                        "sender_type": new_msg.sender_type,
                        "sender_user_id": str(new_msg.sender_user_id) if new_msg.sender_user_id else None,
                        "sender_client_id": str(new_msg.sender_client_id) if new_msg.sender_client_id else None,
                        "content": new_msg.content,
                        "created_at": new_msg.created_at.isoformat()
                    }
                    await manager.broadcast_to_project(project_id, msg_dict)
                    
            except json.JSONDecodeError:
                pass
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)
