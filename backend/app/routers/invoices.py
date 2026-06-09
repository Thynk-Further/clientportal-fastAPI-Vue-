from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoicePayResponse
from app.models.user import User
from app.models.project import Project
from app.models.client import Client
from app.models.invoice import Invoice
from app.models.client_session import ClientSession
from app.services.stripe_service import create_customer, create_invoice

router = APIRouter(tags=["invoices"])

@router.get(
    "/projects/{project_id}/invoices",
    response_model=List[InvoiceRead],
    summary="List invoices for a project"
)
async def list_invoices(
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
        select(Invoice).where(Invoice.project_id == project_id).order_by(Invoice.created_at.desc())
    )
    return result.scalars().all()

@router.post(
    "/invoices",
    response_model=InvoiceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new invoice"
)
async def create_new_invoice(
    invoice_data: InvoiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Project).where(Project.id == invoice_data.project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    result = await db.execute(select(Client).where(Client.id == project.client_id))
    client = result.scalar_one_or_none()

    stripe_customer_id = create_customer(client.email, client.name)

    metadata = {
        "project_id": str(project.id),
        "client_id": str(client.id),
        "user_id": str(current_user.id)
    }
    
    stripe_invoice_id, stripe_payment_intent_id, _ = create_invoice(
        customer_id=stripe_customer_id,
        amount_cents=invoice_data.amount_cents,
        currency="usd",
        metadata=metadata
    )

    line_items_dict = [item.model_dump() for item in invoice_data.line_items]
    time_entry_ids_list = [str(t_id) for t_id in invoice_data.time_entry_ids] if invoice_data.time_entry_ids else []

    db_invoice = Invoice(
        project_id=project.id,
        user_id=current_user.id,
        client_id=client.id,
        stripe_invoice_id=stripe_invoice_id,
        stripe_payment_intent_id=stripe_payment_intent_id,
        amount_cents=invoice_data.amount_cents,
        currency="usd",
        status="draft",
        line_items=line_items_dict,
        time_entry_ids=time_entry_ids_list,
        due_date=invoice_data.due_date
    )
    db.add(db_invoice)
    await db.commit()
    await db.refresh(db_invoice)

    return db_invoice

@router.post(
    "/invoices/{invoice_id}/send",
    response_model=InvoiceRead,
    summary="Mark invoice as sent"
)
async def send_invoice(
    invoice_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Invoice).where(Invoice.id == invoice_id, Invoice.user_id == current_user.id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    invoice.status = "sent"
    await db.commit()
    await db.refresh(invoice)
    
    return invoice

@router.get(
    "/portal/invoices/{invoice_id}/pay",
    response_model=InvoicePayResponse,
    summary="Get payment intent secret for client portal"
)
async def get_payment_secret(
    invoice_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    session_token = request.cookies.get("cp_session")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated as client")
        
    result = await db.execute(select(ClientSession).where(ClientSession.session_token == session_token))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
        
    result = await db.execute(
        select(Invoice).where(Invoice.id == invoice_id, Invoice.client_id == session.client_id)
    )
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    import stripe
    from app.config import settings
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if not settings.STRIPE_SECRET_KEY:
        return InvoicePayResponse(client_secret="mock_secret_123")

    try:
        pi = stripe.PaymentIntent.retrieve(invoice.stripe_payment_intent_id)
        return InvoicePayResponse(client_secret=pi.client_secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve payment intent: {str(e)}")
