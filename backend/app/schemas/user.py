from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
import uuid

class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    logo_url: Optional[str]
    brand_primary_color: Optional[str]
    brand_secondary_color: Optional[str]
    subscription_tier: str
    default_hourly_rate_cents: Optional[int]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "email": "hello@acme.com",
                "full_name": "Jane Doe",
                "logo_url": "https://clientportal-uploads.r2.../logo.png",
                "brand_primary_color": "#2563EB",
                "brand_secondary_color": "#1E3A8A",
                "subscription_tier": "free",
                "default_hourly_rate_cents": 15000
            }
        }
    )

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    logo_url: Optional[str] = None
    brand_primary_color: Optional[str] = Field(None, pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")
    brand_secondary_color: Optional[str] = Field(None, pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")
    default_hourly_rate_cents: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Jane Doe Updated",
                "brand_primary_color": "#FF0000"
            }
        }
    )
