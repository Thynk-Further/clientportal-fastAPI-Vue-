import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    client_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=True)
    
    notification_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    link_url: Mapped[str | None] = mapped_column(String, nullable=True)
    
    read_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    email_sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_notifications_user_read", "user_id", "read_at"),
        Index("idx_notifications_client_read", "client_id", "read_at"),
        Index("idx_notifications_entity", "entity_type", "entity_id"),
        Index("idx_notifications_created_at", created_at.desc()),
    )

    user = relationship("User")
    client = relationship("Client")
