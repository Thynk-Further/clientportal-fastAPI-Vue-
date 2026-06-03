import uuid
from datetime import datetime, date
from sqlalchemy import String, Integer, DateTime, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID, JSON as JSONB
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"))
    stripe_invoice_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(String, nullable=True)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False, default="usd")
    status: Mapped[str] = mapped_column(String, nullable=False, default="draft")
    line_items: Mapped[list | dict] = mapped_column(JSONB, nullable=False, default=list)
    time_entry_ids: Mapped[list | dict] = mapped_column(JSONB, nullable=False, default=list)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="invoices")
    user = relationship("User", back_populates="invoices")
    client = relationship("Client", back_populates="invoices")
    time_entries = relationship("TimeEntry", back_populates="invoice")
