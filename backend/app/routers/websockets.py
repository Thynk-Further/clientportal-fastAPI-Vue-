import uuid
import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies.db import get_db
from app.services.websocket_manager import manager
from app.services.auth_service import decode_access_token
from app.models.client_session import ClientSession
from app.models.message import Message
from app.models.project import Project

router = APIRouter(tags=["websockets"])

@router.websocket("/ws/projects/{project_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    project_id: uuid.UUID, 
    token: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    # Authenticate token
    sender_type = None
    sender_user_id = None
    sender_client_id = None

    # First check if it's a freelancer JWT
    if token:
        payload = decode_access_token(token)
        if payload and "sub" in payload:
            sender_type = "freelancer"
            sender_user_id = uuid.UUID(payload["sub"])
    
    if not sender_type:
        # Check if it's a client session token via cookies
        session_token = websocket.cookies.get("cp_session")
        if session_token:
            result = await db.execute(select(ClientSession).where(ClientSession.session_token == session_token))
            session = result.scalar_one_or_none()
            if session and session.expires_at > datetime.datetime.utcnow():
                sender_type = "client"
                sender_client_id = session.client_id
                
    if not sender_type:
        await websocket.close(code=1008, reason="Invalid or expired token")
        return

    # Verify project exists and user/client has access
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        await websocket.close(code=1008, reason="Project not found")
        return

    if sender_type == "freelancer" and project.user_id != sender_user_id:
        await websocket.close(code=1008, reason="Not authorized for this project")
        return
        
    if sender_type == "client" and project.client_id != sender_client_id:
        await websocket.close(code=1008, reason="Not authorized for this project")
        return

    project_str = str(project_id)
    await manager.connect(websocket, project_str)

    try:
        while True:
            data = await websocket.receive_text()
            
            # Save to DB
            new_msg = Message(
                project_id=project_id,
                sender_type=sender_type,
                sender_user_id=sender_user_id,
                sender_client_id=sender_client_id,
                content=data
            )
            db.add(new_msg)
            await db.commit()
            await db.refresh(new_msg)

            # Broadcast
            message_data = {
                "id": str(new_msg.id),
                "project_id": str(new_msg.project_id),
                "sender_type": new_msg.sender_type,
                "sender_user_id": str(new_msg.sender_user_id) if new_msg.sender_user_id else None,
                "sender_client_id": str(new_msg.sender_client_id) if new_msg.sender_client_id else None,
                "content": new_msg.content,
                "created_at": new_msg.created_at.isoformat()
            }
            await manager.broadcast_to_project(project_str, message_data)

    except WebSocketDisconnect:
        manager.disconnect(websocket, project_str)
