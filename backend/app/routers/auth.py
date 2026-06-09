from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import datetime as dt
import uuid

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.services import auth_service
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, PortalValidateRequest
from app.models.user import User
from app.models.client import Client
from app.models.client_session import ClientSession

router = APIRouter(tags=["auth"])

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new freelancer",
    description="Creates a new freelancer account and returns an access token pair.",
    responses={
        400: {"description": "EMAIL_ALREADY_REGISTERED"}
    }
)
async def register(request: RegisterRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == request.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail={"detail": "Email already registered", "code": "EMAIL_ALREADY_REGISTERED"}
        )
        
    hashed_pwd = auth_service.get_password_hash(request.password)
    user = User(
        email=request.email,
        hashed_password=hashed_pwd,
        full_name=request.full_name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    access_token = auth_service.create_access_token({"sub": str(user.id), "email": user.email, "tier": user.subscription_tier})
    refresh_token = auth_service.create_refresh_token({"sub": str(user.id)})
    
    response.set_cookie(
        key="cp_refresh",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60
    )
    
    return TokenResponse(access_token=access_token)

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Freelancer login",
    description="Authenticates a freelancer and returns an access token. Refresh token is set in an HttpOnly cookie.",
    responses={
        401: {"description": "INVALID_CREDENTIALS"}
    }
)
async def login(request: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if not user or not auth_service.verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail={"detail": "Invalid credentials", "code": "INVALID_CREDENTIALS"}
        )
        
    access_token = auth_service.create_access_token({"sub": str(user.id), "email": user.email, "tier": user.subscription_tier})
    refresh_token = auth_service.create_refresh_token({"sub": str(user.id)})
    
    response.set_cookie(
        key="cp_refresh",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60
    )
    
    return TokenResponse(access_token=access_token)

@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Uses the refresh token from cookies to issue a new access and refresh token pair.",
    responses={
        401: {"description": "INVALID_REFRESH_TOKEN"}
    }
)
async def refresh_token(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("cp_refresh")
    if not token:
        raise HTTPException(
            status_code=401,
            detail={"detail": "Refresh token missing", "code": "INVALID_REFRESH_TOKEN"}
        )
        
    payload = auth_service.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail={"detail": "Invalid or expired refresh token", "code": "INVALID_REFRESH_TOKEN"}
        )
        
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=401,
            detail={"detail": "Invalid refresh token payload", "code": "INVALID_REFRESH_TOKEN"}
        )
        
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=401, detail={"detail": "Invalid ID", "code": "INVALID_REFRESH_TOKEN"})

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=401, detail={"detail": "User not found", "code": "INVALID_REFRESH_TOKEN"})
        
    access_token = auth_service.create_access_token({"sub": str(user.id), "email": user.email, "tier": user.subscription_tier})
    new_refresh_token = auth_service.create_refresh_token({"sub": str(user.id)})
    
    response.set_cookie(
        key="cp_refresh",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60
    )
    
    return TokenResponse(access_token=access_token)

@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout freelancer",
    description="Invalidates the refresh token by clearing the cookie."
)
async def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie(key="cp_refresh", httponly=True, secure=True, samesite="strict")
    return None

@router.post(
    "/portal/validate",
    status_code=status.HTTP_200_OK,
    summary="Validate client portal token",
    description="Validates a magic link portal token and issues an HttpOnly cp_session cookie for subsequent portal access.",
    responses={
        404: {"description": "INVALID_PORTAL_TOKEN"}
    }
)
async def validate_portal_token(request: PortalValidateRequest, response: Response, db: AsyncSession = Depends(get_db)):
    # Check if primary client token
    result = await db.execute(select(Client).where(Client.portal_token == request.portal_token))
    client = result.scalar_one_or_none()
    
    client_member = None
    if not client:
        # Check if team member token
        from app.models.client_member import ClientMember
        member_result = await db.execute(select(ClientMember).where(ClientMember.member_token == request.portal_token))
        client_member = member_result.scalar_one_or_none()
        
        if not client_member:
            raise HTTPException(
                status_code=404,
                detail={"detail": "Invalid or expired portal token", "code": "INVALID_PORTAL_TOKEN"}
            )
        client_id = client_member.client_id
    else:
        client_id = client.id
        
    session_token = str(uuid.uuid4())
    expires = dt.datetime.utcnow() + dt.timedelta(days=7)
    
    client_session = ClientSession(
        client_id=client_id,
        client_member_id=client_member.id if client_member else None,
        session_token=session_token,
        expires_at=expires
    )
    db.add(client_session)
    await db.commit()
    
    response.set_cookie(
        key="cp_session",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60
    )
    
    return {"status": "ok"}
