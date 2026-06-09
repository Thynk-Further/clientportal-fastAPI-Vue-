from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import boto3
from botocore.config import Config
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.config import settings
from app.schemas.file import PresignedUrlRequest, PresignedUrlResponse, FileUploadConfirm, FileUploadRead
from app.models.user import User
from app.models.deliverable import Deliverable
from app.models.project import Project
from app.models.file_upload import FileUpload
from app.services.notifications_service import create_notification

router = APIRouter(tags=["files"])

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.R2_ENDPOINT_URL,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto"
    )

@router.post(
    "/presigned-url",
    response_model=PresignedUrlResponse,
    summary="Generate presigned upload URL",
    description="Generates a temporary R2 PUT URL for a file."
)
async def generate_presigned_url(request: PresignedUrlRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verify the user has access to this deliverable
    result = await db.execute(
        select(Deliverable)
        .join(Project, Deliverable.project_id == Project.id)
        .where(Deliverable.id == request.deliverable_id, Project.user_id == current_user.id)
    )
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found or access denied")

    # Generate a unique object key: {user_id}/{project_id}/{deliverable_id}/{uuid}_{filename}
    file_uuid = uuid.uuid4()
    safe_filename = request.filename.replace(" ", "_")
    object_key = f"{current_user.id}/{deliverable.project_id}/{deliverable.id}/{file_uuid}_{safe_filename}"

    s3_client = get_s3_client()
    try:
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.R2_BUCKET_NAME,
                "Key": object_key,
                "ContentType": request.content_type
            },
            ExpiresIn=900 # 15 minutes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")

    return PresignedUrlResponse(presigned_url=presigned_url, object_key=object_key)

@router.post(
    "/confirm",
    response_model=FileUploadRead,
    status_code=status.HTTP_201_CREATED,
    summary="Confirm file upload",
    description="Saves the file metadata to the database after successful R2 upload."
)
async def confirm_file_upload(
    request: FileUploadConfirm,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify access to deliverable again
    result = await db.execute(
        select(Deliverable, Project.client_id, Deliverable.name)
        .join(Project, Deliverable.project_id == Project.id)
        .where(Deliverable.id == request.deliverable_id, Project.user_id == current_user.id)
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Deliverable not found or access denied")
        
    deliverable, client_id, deliverable_name = row

    file_upload = FileUpload(
        deliverable_id=request.deliverable_id,
        uploaded_by_user_id=current_user.id,
        file_name=request.file_name,
        object_key=request.object_key,
        file_size=request.file_size,
        mime_type=request.mime_type
    )

    db.add(file_upload)
    await db.commit()
    await db.refresh(file_upload)

    if client_id:
        await create_notification(
            db=db,
            background_tasks=background_tasks,
            recipient_type="client",
            recipient_id=client_id,
            notification_type="deliverable_uploaded",
            entity_type="deliverable",
            entity_id=deliverable.id,
            title="New File Uploaded",
            message=f"{current_user.full_name} uploaded a new file to {deliverable_name}",
            link_url=f"/portal/{deliverable.project_id}",
            project_id=deliverable.project_id
        )

    return file_upload
