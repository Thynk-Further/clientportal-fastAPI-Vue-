import uuid
from datetime import datetime
from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID
from app.database import Base

class TimeEntry(Base):
    __tablename__ = "time_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    deliverable_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("deliverables.id", ondelete="CASCADE"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_billable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    hourly_rate_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    invoice_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_time_entries_user_running", "user_id", "ended_at"),
        Index("idx_time_entries_unbilled", "project_id", "is_billable"),
    )

    project = relationship("Project", back_populates="time_entries")
    deliverable = relationship("Deliverable", back_populates="time_entries")
    user = relationship("User", back_populates="time_entries")
    invoice = relationship("Invoice", back_populates="time_entries")
