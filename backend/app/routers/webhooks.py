from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import stripe
import json

from app.dependencies.db import get_db
from app.config import settings
from app.models.invoice import Invoice

router = APIRouter(tags=["webhooks"])

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not settings.STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Event.construct_from(
                json.loads(payload.decode('utf-8')),
                stripe.api_key
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Webhook Error")
    else:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "invoice.paid":
        stripe_invoice = event["data"]["object"]
        stripe_invoice_id = stripe_invoice.get("id")
        
        if stripe_invoice_id:
            result = await db.execute(
                select(Invoice).where(Invoice.stripe_invoice_id == stripe_invoice_id)
            )
            db_invoice = result.scalar_one_or_none()
            if db_invoice:
                db_invoice.status = "paid"
                db_invoice.paid_at = datetime.utcnow()
                await db.commit()

    return {"status": "success"}
