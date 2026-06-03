import uuid
from datetime import datetime
from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    onboarding_video_url: Mapped[str | None] = mapped_column(String, nullable=True)
    onboarding_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    show_onboarding: Mapped[bool] = mapped_column(Boolean, default=False)
    default_hourly_rate_cents: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_projects_user_status", "user_id", "status"),
    )

    user = relationship("User", back_populates="projects")
    client = relationship("Client", back_populates="projects")
    deliverables = relationship("Deliverable", back_populates="project")
    messages = relationship("Message", back_populates="project")
    invoices = relationship("Invoice", back_populates="project")
    time_entries = relationship("TimeEntry", back_populates="project")
    form_submissions = relationship("FormSubmission", back_populates="project")
