from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    display_name: str


class UserCreate(UserBase):
    password: Optional[str] = None
    google_id: Optional[str] = None


class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    display_name: str


class UserLinkBase(BaseModel):
    link_type: str
    url: str


class UserLinkResponse(UserLinkBase):
    id: int
    
    class Config:
        from_attributes = True


class UserProfileResponse(UserResponse):
    links: List[UserLinkResponse] = []


class PostBase(BaseModel):
    caption: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user_id: int
    image_url_display_1: str
    image_url_display_2: str
    image_url_full_1: str
    image_url_full_2: str
    created_at: datetime
    author: UserResponse
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str


class EmailChange(BaseModel):
    new_email: EmailStr


class LinksUpdate(BaseModel):
    links: List[UserLinkBase]
