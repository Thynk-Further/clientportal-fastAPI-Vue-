import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID
from app.database import Base

class FormResponse(Base):
    __tablename__ = "form_responses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_submission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("form_submissions.id", ondelete="CASCADE"), index=True)
    form_field_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("form_fields.id", ondelete="CASCADE"))
    value_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    value_file_url: Mapped[str | None] = mapped_column(String, nullable=True)
    value_file_object_key: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    submission = relationship("FormSubmission", back_populates="responses")
    field = relationship("FormField", back_populates="responses")
