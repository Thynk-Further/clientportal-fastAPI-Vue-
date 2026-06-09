from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.schemas.client import ClientCreate, ClientReadList, ClientReadDetail, ClientUpdate
from app.models.user import User
from app.models.client import Client
from app.models.client_session import ClientSession
from app.services.email_service import send_magic_link
from app.config import settings

router = APIRouter(tags=["clients"])

@router.get(
    "",
    response_model=List[ClientReadList],
    summary="List clients",
    description="List all clients owned by the authenticated freelancer."
)
async def list_clients(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Client).where(Client.user_id == current_user.id).order_by(Client.created_at.desc()))
    return result.scalars().all()

@router.post(
    "",
    response_model=ClientReadDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Create a client",
    description="Creates a new client, generates a portal token, and sends a magic link email to the client."
)
async def create_client(
    client_data: ClientCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Client).where(Client.user_id == current_user.id, Client.email == client_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Client with this email already exists")

    client = Client(
        user_id=current_user.id,
        name=client_data.name,
        email=client_data.email,
        company_name=client_data.company_name,
        phone=client_data.phone,
        address=client_data.address
    )
    db.add(client)
    await db.commit()
    await db.refresh(client)

    portal_url = f"{settings.FRONTEND_URL}/portal/{client.portal_token}"
    background_tasks.add_task(send_magic_link, client.email, portal_url, client.name, current_user.full_name)

    return client

@router.get(
    "/{client_id}",
    response_model=ClientReadDetail,
    summary="Get client details",
    description="Returns full client details including the portal token."
)
async def get_client(client_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Client).where(Client.id == client_id, Client.user_id == current_user.id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.patch(
    "/{client_id}",
    response_model=ClientReadDetail,
    summary="Update a client"
)
async def update_client(
    client_id: uuid.UUID,
    client_data: ClientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Client).where(Client.id == client_id, Client.user_id == current_user.id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if client_data.name is not None:
        client.name = client_data.name
    if client_data.email is not None:
        # Check if new email is taken
        if client_data.email != client.email:
            existing = await db.execute(select(Client).where(Client.user_id == current_user.id, Client.email == client_data.email))
            if existing.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Client with this email already exists")
        client.email = client_data.email
    if client_data.company_name is not None:
        client.company_name = client_data.company_name
    if client_data.phone is not None:
        client.phone = client_data.phone
    if client_data.address is not None:
        client.address = client_data.address

    await db.commit()
    await db.refresh(client)
    return client

@router.post(
    "/{client_id}/resend-link",
    status_code=status.HTTP_200_OK,
    summary="Resend magic link",
    description="Regenerates the portal token, invalidates existing sessions, and resends the magic link email."
)
async def resend_link(
    client_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Client).where(Client.id == client_id, Client.user_id == current_user.id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.portal_token = str(uuid.uuid4())
    
    await db.execute(delete(ClientSession).where(ClientSession.client_id == client.id))
    
    await db.commit()
    await db.refresh(client)

    portal_url = f"{settings.FRONTEND_URL}/portal/{client.portal_token}"
    background_tasks.add_task(send_magic_link, client.email, portal_url, client.name, current_user.full_name)

    return {"status": "ok", "message": "Magic link regenerated and sent"}
