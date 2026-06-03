import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID
from app.database import Base

class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("form_templates.id", ondelete="CASCADE"))
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_form_submissions_status", "project_id", "status"),
    )

    template = relationship("FormTemplate", back_populates="submissions")
    project = relationship("Project", back_populates="form_submissions")
    client = relationship("Client", back_populates="form_submissions")
    responses = relationship("FormResponse", back_populates="submission", cascade="all, delete-orphan")
