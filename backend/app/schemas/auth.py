from pydantic import BaseModel, ConfigDict
import uuid

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "hello@acme.com",
                "password": "strongpassword123",
                "full_name": "Jane Doe"
            }
        }
    )

class LoginRequest(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "hello@acme.com",
                "password": "strongpassword123"
            }
        }
    )

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )

class PortalValidateRequest(BaseModel):
    portal_token: uuid.UUID

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "portal_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
            }
        }
    )
