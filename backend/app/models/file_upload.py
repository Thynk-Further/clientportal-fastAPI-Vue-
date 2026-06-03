import uuid
from datetime import datetime
from sqlalchemy import String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Uuid as UUID
from app.database import Base

class FileUpload(Base):
    __tablename__ = "file_uploads"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deliverable_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("deliverables.id", ondelete="CASCADE"), index=True)
    uploaded_by_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_url: Mapped[str | None] = mapped_column(String, nullable=True)
    object_key: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    deliverable = relationship("Deliverable", back_populates="file_uploads")
    uploaded_by = relationship("User")
