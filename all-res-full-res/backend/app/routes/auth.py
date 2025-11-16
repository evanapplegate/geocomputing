from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
from hashlib import sha256
from app.database import get_db
from app.models import User, PasswordResetToken
from app.schemas import Token, PasswordResetRequest, PasswordReset, UserResponse
from app.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.email_service import send_password_reset_email

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/google", response_model=Token)
async def google_auth(google_token: str, db: Session = Depends(get_db)):
    """Verify Google token and create/return user"""
    # In production, verify token with Google API
    # For now, simplified version - you'd use google-auth library
    # This is a placeholder - implement proper Google OAuth verification
    raise HTTPException(
        status_code=501,
        detail="Google OAuth not fully implemented - use google-auth library to verify token"
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Email/password login"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/reset-password", status_code=200)
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset"""
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        # Generate secure token
        token = secrets.token_urlsafe(32)
        token_hash = sha256(token.encode()).hexdigest()
        
        # Store token
        reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        db.add(reset_token)
        db.commit()
        
        # Send email
        send_password_reset_email(user.email, token)
    
    # Always return success (don't reveal if email exists)
    return {"message": "If email exists, reset link has been sent"}


@router.post("/reset-password/complete", status_code=200)
async def complete_password_reset(
    reset: PasswordReset,
    db: Session = Depends(get_db)
):
    """Complete password reset"""
    token_hash = sha256(reset.token.encode()).hexdigest()
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_hash,
        PasswordResetToken.used == False,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()
    
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    user.password_hash = get_password_hash(reset.new_password)
    reset_token.used = True
    db.commit()
    
    return {"message": "Password reset successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout", status_code=200)
async def logout():
    """Logout (client should discard token)"""
    return {"message": "Logged out"}
