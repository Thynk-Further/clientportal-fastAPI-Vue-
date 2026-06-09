import stripe
from app.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_customer(email: str, name: str) -> str:
    if not settings.STRIPE_SECRET_KEY:
        return f"mock_cus_{email}"
        
    customer = stripe.Customer.create(
        email=email,
        name=name
    )
    return customer.id

def create_invoice(customer_id: str, amount_cents: int, currency: str = "usd", metadata: dict = None) -> tuple[str, str, str]:
    if not settings.STRIPE_SECRET_KEY:
        return "mock_in_123", "mock_pi_123", "mock_secret_123"

    stripe.InvoiceItem.create(
        customer=customer_id,
        amount=amount_cents,
        currency=currency,
        description="ClientPortal Project Services"
    )

    invoice = stripe.Invoice.create(
        customer=customer_id,
        auto_advance=True,
        collection_method="charge_automatically",
        metadata=metadata or {}
    )

    invoice = stripe.Invoice.finalize_invoice(invoice.id)
    
    payment_intent_id = invoice.payment_intent
    
    if payment_intent_id:
        if isinstance(payment_intent_id, str):
            pi = stripe.PaymentIntent.retrieve(payment_intent_id)
            client_secret = pi.client_secret
        else:
            client_secret = payment_intent_id.client_secret
            payment_intent_id = payment_intent_id.id
    else:
        client_secret = None

    return invoice.id, payment_intent_id, client_secret
