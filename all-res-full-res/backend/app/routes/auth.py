from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
from hashlib import sha256
import base64
from app.database import get_db
from app.models import User, PasswordResetToken
from app.schemas import Token, PasswordResetRequest, PasswordReset, UserResponse
from app.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.email_service import send_password_reset_email
from app.logger import log_auth_event, log_error

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/google")
async def google_auth_initiate():
    """Initiate Google OAuth flow"""
    from app.config import settings
    import urllib.parse
    
    # Construct backend URL for callback
    if 'localhost' in settings.frontend_url:
        backend_url = settings.frontend_url.replace(':3000', ':8000')
    else:
        # Production: use same domain or configure separately
        backend_url = settings.frontend_url.replace('https://', 'https://api.') if 'https://' in settings.frontend_url else settings.frontend_url
    redirect_uri = f"{backend_url}/api/auth/google/callback"
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    return {"auth_url": auth_url}


@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    """Handle Google OAuth callback"""
    from app.config import settings
    import httpx
    
    # Construct backend URL for callback
    if 'localhost' in settings.frontend_url:
        backend_url = settings.frontend_url.replace(':3000', ':8000')
    else:
        backend_url = settings.frontend_url.replace('https://', 'https://api.') if 'https://' in settings.frontend_url else settings.frontend_url
    
    # Exchange code for token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": f"{backend_url}/api/auth/google/callback",
        "grant_type": "authorization_code"
    }
    
    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code")
        
        tokens = token_response.json()
        access_token = tokens["access_token"]
        
        # Get user info
        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = user_info_response.json()
        
        # Create or update user
        user = db.query(User).filter(User.google_id == user_info["id"]).first()
        if not user:
            user = db.query(User).filter(User.email == user_info["email"]).first()
            if user:
                user.google_id = user_info["id"]
            else:
                user = User(
                    email=user_info["email"],
                    google_id=user_info["id"],
                    display_name=user_info.get("name", user_info["email"].split("@")[0])
                )
                db.add(user)
        else:
            user.email = user_info["email"]
            user.display_name = user_info.get("name", user.display_name)
        
        db.commit()
        db.refresh(user)
        
        # Create JWT token
        from app.auth import create_access_token
        from datetime import timedelta
        access_token_jwt = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(days=7)
        )
        
        # Redirect to frontend with token
        from fastapi.responses import RedirectResponse
        return RedirectResponse(
            url=f"{settings.frontend_url}/app?token={access_token_jwt}"
        )


@router.get("/github")
async def github_auth_initiate():
    """Initiate GitHub OAuth flow"""
    from app.config import settings
    import urllib.parse
    
    # Construct backend URL for callback
    if 'localhost' in settings.frontend_url:
        backend_url = settings.frontend_url.replace(':3000', ':8000')
    else:
        # Production: use same domain or configure separately
        backend_url = settings.frontend_url.replace('https://', 'https://api.') if 'https://' in settings.frontend_url else settings.frontend_url
    redirect_uri = f"{backend_url}/api/auth/github/callback"
    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": redirect_uri,
        "scope": "user:email"
    }
    auth_url = f"https://github.com/login/oauth/authorize?{urllib.parse.urlencode(params)}"
    return {"auth_url": auth_url}


@router.get("/github/callback")
async def github_callback(code: str, db: Session = Depends(get_db)):
    """Handle GitHub OAuth callback"""
    from app.config import settings
    import httpx
    
    # Construct backend URL for callback
    if 'localhost' in settings.frontend_url:
        backend_url = settings.frontend_url.replace(':3000', ':8000')
    else:
        backend_url = settings.frontend_url.replace('https://', 'https://api.') if 'https://' in settings.frontend_url else settings.frontend_url
    
    # Exchange code for token
    token_url = "https://github.com/login/oauth/access_token"
    data = {
        "code": code,
        "client_id": settings.github_client_id,
        "client_secret": settings.github_client_secret,
        "redirect_uri": f"{backend_url}/api/auth/github/callback"
    }
    headers = {"Accept": "application/json"}
    
    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data, headers=headers)
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code")
        
        tokens = token_response.json()
        access_token = tokens["access_token"]
        
        # Get user info
        user_info_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"}
        )
        user_info = user_info_response.json()
        
        # Get email
        email_response = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"token {access_token}"}
        )
        emails = email_response.json()
        email = next((e["email"] for e in emails if e["primary"]), emails[0]["email"] if emails else None)
        
        if not email:
            raise HTTPException(status_code=400, detail="No email found")
        
        # Create or update user
        user = db.query(User).filter(User.github_id == str(user_info["id"])).first()
        if not user:
            user = db.query(User).filter(User.email == email).first()
            if user:
                user.github_id = str(user_info["id"])
            else:
                user = User(
                    email=email,
                    github_id=str(user_info["id"]),
                    display_name=user_info.get("name", user_info["login"])
                )
                db.add(user)
        else:
            user.email = email
            user.display_name = user_info.get("name", user.display_name)
        
        db.commit()
        db.refresh(user)
        
        # Create JWT token
        from app.auth import create_access_token
        from datetime import timedelta
        access_token_jwt = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(days=7)
        )
        
        # Redirect to frontend with token
        from fastapi.responses import RedirectResponse
        return RedirectResponse(
            url=f"{settings.frontend_url}/app?token={access_token_jwt}"
        )


@router.get("/x")
async def x_auth_initiate():
    """Initiate X/Twitter OAuth flow"""
    from app.config import settings
    import urllib.parse
    
    # Construct backend URL for callback
    if 'localhost' in settings.frontend_url:
        backend_url = settings.frontend_url.replace(':3000', ':8000')
    else:
        backend_url = settings.frontend_url.replace('https://', 'https://api.') if 'https://' in settings.frontend_url else settings.frontend_url
    
    # X OAuth 2.0 uses PKCE
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(sha256(code_verifier.encode()).digest()).decode().rstrip('=')
    
    redirect_uri = f"{backend_url}/api/auth/x/callback"
    params = {
        "response_type": "code",
        "client_id": settings.x_client_id,
        "redirect_uri": redirect_uri,
        "scope": "tweet.read users.read offline.access",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": secrets.token_urlsafe(16)
    }
    auth_url = f"https://twitter.com/i/oauth2/authorize?{urllib.parse.urlencode(params)}"
    return {"auth_url": auth_url, "code_verifier": code_verifier}


@router.get("/x/callback")
async def x_callback(code: str, state: str, db: Session = Depends(get_db)):
    """Handle X/Twitter OAuth callback"""
    from app.config import settings
    import httpx
    
    # Construct backend URL for callback
    if 'localhost' in settings.frontend_url:
        backend_url = settings.frontend_url.replace(':3000', ':8000')
    else:
        backend_url = settings.frontend_url.replace('https://', 'https://api.') if 'https://' in settings.frontend_url else settings.frontend_url
    
    try:
        # Exchange code for token (simplified - in production, store code_verifier in session)
        token_url = "https://api.twitter.com/2/oauth2/token"
        client_creds = base64.b64encode(f"{settings.x_client_id}:{settings.x_client_secret}".encode()).decode()
        
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": settings.x_client_id,
            "redirect_uri": f"{backend_url}/api/auth/x/callback",
            "code_verifier": "temp"  # Should be retrieved from session
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                token_url,
                data=data,
                headers={"Authorization": f"Basic {client_creds}", "Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if token_response.status_code != 200:
                log_error(Exception(f"X OAuth token exchange failed: {token_response.text}"), "X_AUTH")
                raise HTTPException(status_code=400, detail="Failed to exchange code")
            
            tokens = token_response.json()
            access_token = tokens["access_token"]
            
            # Get user info
            user_info_response = await client.get(
                "https://api.twitter.com/2/users/me?user.fields=username,name,profile_image_url",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if user_info_response.status_code != 200:
                log_error(Exception(f"X user info failed: {user_info_response.text}"), "X_AUTH")
                raise HTTPException(status_code=400, detail="Failed to get user info")
            
            user_info = user_info_response.json()["data"]
            x_id = user_info["id"]
            username = user_info.get("username", "")
            name = user_info.get("name", username)
            
            # Create or update user
            user = db.query(User).filter(User.x_id == x_id).first()
            if not user:
                # Try to find by email (X doesn't provide email in OAuth 2.0)
                # Use username@x.com as placeholder
                email = f"{username}@x.com"
                user = db.query(User).filter(User.email == email).first()
                if user:
                    user.x_id = x_id
                else:
                    user = User(
                        email=email,
                        x_id=x_id,
                        display_name=name
                    )
                    db.add(user)
            else:
                user.display_name = name
            
            db.commit()
            db.refresh(user)
            
            log_auth_event("X_LOGIN_SUCCESS", user.id, f"username: {username}")
            
            # Create JWT token
            from app.auth import create_access_token
            from datetime import timedelta
            access_token_jwt = create_access_token(
                data={"sub": user.id},
                expires_delta=timedelta(days=7)
            )
            
            # Redirect to frontend with token
            from fastapi.responses import RedirectResponse
            return RedirectResponse(
                url=f"{settings.frontend_url}/app?token={access_token_jwt}"
            )
    except Exception as e:
        log_error(e, "X_AUTH_CALLBACK")
        raise HTTPException(status_code=500, detail="Authentication failed")


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Email/password login"""
    try:
        user = db.query(User).filter(User.email == form_data.username).first()
        if not user or not user.password_hash:
            log_auth_event("LOGIN_FAILED", None, f"email: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        if not verify_password(form_data.password, user.password_hash):
            log_auth_event("LOGIN_FAILED", user.id, "invalid password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        log_auth_event("LOGIN_SUCCESS", user.id)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "LOGIN")
        raise HTTPException(status_code=500, detail="Login failed")


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
