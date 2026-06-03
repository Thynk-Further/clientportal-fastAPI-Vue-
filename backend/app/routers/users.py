from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.schemas.user import UserRead, UserUpdate
from app.models.user import User

router = APIRouter(tags=["users"])

@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user profile",
    description="Returns the profile details and subscription tier for the currently authenticated freelancer."
)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch(
    "/me",
    response_model=UserRead,
    summary="Update current user profile",
    description="Updates branding, name, and default hourly rate for the freelancer."
)
async def update_me(
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        setattr(current_user, key, value)
        
    await db.commit()
    await db.refresh(current_user)
    
    return current_user
