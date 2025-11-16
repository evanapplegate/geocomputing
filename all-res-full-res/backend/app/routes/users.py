from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, UserLink, Post
from app.schemas import (
    UserProfileResponse, UserLinkResponse, EmailChange,
    UserResponse, PostResponse, LinksUpdate, UserUpdate
)
from app.auth import get_current_user, get_password_hash
from app.r2_storage import upload_avatar
from app.email_service import send_email_verification
import secrets
from hashlib import sha256
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile with links"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    current_user.display_name = user_update.display_name
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/me/avatar", response_model=UserResponse)
async def upload_avatar_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload user avatar"""
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, and WebP images are allowed"
        )
    
    image_data = await file.read()
    if len(image_data) > 10 * 1024 * 1024:  # 10MB max
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size must be less than 10MB"
        )
    
    try:
        avatar_url = upload_avatar(image_data, current_user.id)
        current_user.avatar_url = avatar_url
        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload avatar: {str(e)}"
        )


@router.put("/me/links", response_model=List[UserLinkResponse])
async def update_profile_links(
    links_update: LinksUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile links"""
    # Delete existing links
    db.query(UserLink).filter(UserLink.user_id == current_user.id).delete()
    
    # Add new links
    for link_data in links_update.links:
        if link_data.url:
            link = UserLink(
                user_id=current_user.id,
                link_type=link_data.link_type,
                url=link_data.url
            )
            db.add(link)
    
    db.commit()
    return db.query(UserLink).filter(UserLink.user_id == current_user.id).all()


@router.put("/me/email", status_code=200)
async def change_email(
    email_change: EmailChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Request email change (sends verification)"""
    # Check if email already exists
    existing = db.query(User).filter(User.email == email_change.new_email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use"
        )
    
    # Generate verification token (simplified - in production use proper token storage)
    token = secrets.token_urlsafe(32)
    # Store token temporarily (you'd want a proper EmailVerificationToken table)
    # For now, just send email
    send_email_verification(email_change.new_email, token)
    
    return {"message": "Verification email sent"}


@router.get("/{username}", response_model=UserProfileResponse)
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    """Get user profile by username (using email for now)"""
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/{username}/posts", response_model=List[PostResponse])
async def get_user_posts(
    username: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get user's posts"""
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    posts = db.query(Post).filter(Post.user_id == user.id).offset(skip).limit(limit).all()
    return posts
