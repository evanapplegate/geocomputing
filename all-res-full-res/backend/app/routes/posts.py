from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.database import get_db
from app.models import Post, User
from app.schemas import PostCreate, PostResponse
from app.auth import get_current_user
from app.r2_storage import upload_image
from app.logger import log_request, log_response, log_upload, log_error

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("/feed", response_model=List[PostResponse])
async def get_feed(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get feed of all posts"""
    try:
        log_request("GET", "/api/posts/feed")
        posts = db.query(Post).order_by(desc(Post.created_at)).offset(skip).limit(limit).all()
        log_response("GET", "/api/posts/feed", 200)
        return posts
    except Exception as e:
        log_error(e, "GET_FEED")
        raise HTTPException(status_code=500, detail="Failed to load feed")


@router.get("/my", response_model=List[PostResponse])
async def get_my_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's posts"""
    try:
        log_request("GET", "/api/posts/my", current_user.id)
        posts = db.query(Post).filter(Post.user_id == current_user.id).order_by(desc(Post.created_at)).all()
        log_response("GET", "/api/posts/my", 200, current_user.id)
        return posts
    except Exception as e:
        log_error(e, "GET_MY_POSTS")
        raise HTTPException(status_code=500, detail="Failed to load posts")


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
    caption: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new post with two images"""
    try:
        log_request("POST", "/api/posts", current_user.id)
        
        # Validate file types
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/tiff", "image/tif"]
        allowed_extensions = ['.cr2', '.nef', '.arw', '.raf', '.orf', '.rw2', '.pef', '.srw', '.dng']
        
        image1_ext = '.' + (image1.filename or '').split('.')[-1].lower() if image1.filename else ''
        image2_ext = '.' + (image2.filename or '').split('.')[-1].lower() if image2.filename else ''
        
        if (image1.content_type not in allowed_types and image1_ext not in allowed_extensions) or \
           (image2.content_type not in allowed_types and image2_ext not in allowed_extensions):
            log_upload(0, image1.content_type or 'unknown', current_user.id, False, "Invalid file type")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, PNG, TIFF, and RAW images are allowed"
            )
        
        # Read image data
        image1_data = await image1.read()
        image2_data = await image2.read()
        
        # Validate file size (10MB minimum, 500MB max)
        min_size = 10 * 1024 * 1024  # 10MB
        max_size = 500 * 1024 * 1024  # 500MB
        if len(image1_data) < min_size or len(image2_data) < min_size:
            log_upload(len(image1_data), image1.content_type or 'unknown', current_user.id, False, "File too small")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image must be at least 10MB. Current sizes: {len(image1_data)/(1024*1024):.2f}MB, {len(image2_data)/(1024*1024):.2f}MB"
            )
        if len(image1_data) > max_size or len(image2_data) > max_size:
            log_upload(len(image1_data), image1.content_type or 'unknown', current_user.id, False, "File too large")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image size must be less than 500MB"
            )
        
        # Create post record first to get ID
        post = Post(
            user_id=current_user.id,
            caption=caption,
            image_url_display_1="",  # Temporary
            image_url_display_2="",
            image_url_full_1="",
            image_url_full_2=""
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        
        # Upload images to R2
        try:
            display_url_1, full_url_1 = upload_image(image1_data, current_user.id, post.id, 1, image1.filename)
            display_url_2, full_url_2 = upload_image(image2_data, current_user.id, post.id, 2, image2.filename)
            
            # Update post with URLs
            post.image_url_display_1 = display_url_1
            post.image_url_display_2 = display_url_2
            post.image_url_full_1 = full_url_1
            post.image_url_full_2 = full_url_2
            db.commit()
            db.refresh(post)
            
            log_upload(len(image1_data), image1.content_type or image1_ext, current_user.id, True)
            log_response("POST", "/api/posts", 201, current_user.id)
            return post
        except Exception as e:
            db.delete(post)
            db.commit()
            log_error(e, "POST_UPLOAD_R2")
            log_upload(len(image1_data), image1.content_type or 'unknown', current_user.id, False, str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload images: {str(e)}"
            )
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "CREATE_POST")
        raise HTTPException(status_code=500, detail="Failed to create post")


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get single post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post


@router.get("/{post_id}/download")
async def download_full_res(post_id: int, db: Session = Depends(get_db)):
    """Get full-resolution download URL"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    # Return direct URL (R2 public URLs)
    return {"url": post.image_url_full_1}


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete post (author only)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
    db.delete(post)
    db.commit()
    return None
