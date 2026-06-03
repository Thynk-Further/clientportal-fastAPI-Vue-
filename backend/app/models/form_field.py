import uuid
from datetime import datetime
from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID, JSON as JSONB
from app.database import Base

class FormField(Base):
    __tablename__ = "form_fields"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form_template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("form_templates.id", ondelete="CASCADE"))
    label: Mapped[str] = mapped_column(String, nullable=False)
    helper_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    field_type: Mapped[str] = mapped_column(String, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    options: Mapped[list | dict | None] = mapped_column(JSONB, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_form_fields_template_id", "form_template_id", "sort_order"),
    )

    template = relationship("FormTemplate", back_populates="fields")
    responses = relationship("FormResponse", back_populates="field")
