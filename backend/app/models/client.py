import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID, JSON as JSONB
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    company_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    portal_token: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    notification_email_prefs: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "email", name="idx_clients_user_email"),
    )

    user = relationship("User", back_populates="clients")
    projects = relationship("Project", back_populates="client")
    sessions = relationship("ClientSession", back_populates="client")
    approvals = relationship("Approval", back_populates="client")
    invoices = relationship("Invoice", back_populates="client")
    form_submissions = relationship("FormSubmission", back_populates="client")
