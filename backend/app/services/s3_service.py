import boto3
from botocore.exceptions import ClientError
from app.config import settings
from typing import Optional

def get_s3_client():
    if not settings.R2_ENDPOINT_URL or not settings.R2_ACCESS_KEY_ID or not settings.R2_SECRET_ACCESS_KEY:
        return None

    return boto3.client(
        's3',
        endpoint_url=settings.R2_ENDPOINT_URL,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name='auto' 
    )

def generate_presigned_put_url(object_key: str, content_type: str, expires_in: int = 900) -> str:
    s3_client = get_s3_client()
    
    if not s3_client:
        print(f"MOCK R2: Would have generated presigned URL for {object_key}")
        return f"http://localhost:8000/mock-upload?key={object_key}"

    try:
        response = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.R2_BUCKET_NAME,
                'Key': object_key,
                'ContentType': content_type
            },
            ExpiresIn=expires_in
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        raise
