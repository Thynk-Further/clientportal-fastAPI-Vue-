from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.schemas.file_upload import PresignedUrlRequest, PresignedUrlResponse, FileUploadCreate, FileUploadRead
from app.models.user import User
from app.models.project import Project
from app.models.deliverable import Deliverable
from app.models.file_upload import FileUpload
from app.services.s3_service import generate_presigned_put_url
from app.config import settings

router = APIRouter(tags=["files"])

@router.post(
    "/presigned-url",
    response_model=PresignedUrlResponse,
    summary="Generate presigned upload URL"
)
async def generate_upload_url(
    request_data: PresignedUrlRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Deliverable)
        .join(Project, Deliverable.project_id == Project.id)
        .where(Deliverable.id == request_data.deliverable_id, Project.user_id == current_user.id)
    )
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    object_key = f"{current_user.id}/{deliverable.project_id}/{deliverable.id}/{uuid.uuid4()}_{request_data.filename}"
    
    url = generate_presigned_put_url(object_key, request_data.content_type)
    
    return PresignedUrlResponse(
        presigned_url=url,
        object_key=object_key
    )

@router.post(
    "/confirm",
    response_model=FileUploadRead,
    status_code=status.HTTP_201_CREATED,
    summary="Confirm file upload"
)
async def confirm_upload(
    upload_data: FileUploadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Deliverable)
        .join(Project, Deliverable.project_id == Project.id)
        .where(Deliverable.id == upload_data.deliverable_id, Project.user_id == current_user.id)
    )
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    filename = upload_data.object_key.split('_', 1)[-1] if '_' in upload_data.object_key else upload_data.object_key
    
    file_url = f"{settings.R2_PUBLIC_URL}/{upload_data.object_key}" if settings.R2_PUBLIC_URL else upload_data.object_key

    file_upload = FileUpload(
        deliverable_id=upload_data.deliverable_id,
        uploaded_by_user_id=current_user.id,
        file_name=filename,
        file_url=file_url,
        object_key=upload_data.object_key,
        file_size=upload_data.file_size,
        mime_type=upload_data.mime_type
    )
    db.add(file_upload)
    await db.commit()
    await db.refresh(file_upload)
    
    return file_upload
