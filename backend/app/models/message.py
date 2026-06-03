import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    deliverable_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("deliverables.id", ondelete="CASCADE"), nullable=True, index=True)
    sender_type: Mapped[str] = mapped_column(String, nullable=False)
    sender_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    sender_client_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_messages_project_time", "project_id", "created_at"),
        Index("idx_messages_deliverable_time", "deliverable_id", "created_at"),
    )

    project = relationship("Project", back_populates="messages")
    deliverable = relationship("Deliverable", back_populates="messages")
    sender_user = relationship("User")
    sender_client = relationship("Client")
