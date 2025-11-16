from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    google_id = Column(String, unique=True, nullable=True, index=True)
    github_id = Column(String, unique=True, nullable=True, index=True)
    display_name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    links = relationship("UserLink", back_populates="user", cascade="all, delete-orphan")
    reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")


class UserLink(Base):
    __tablename__ = "user_links"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    link_type = Column(String, nullable=False)  # 'twitter', 'instagram', 'website'
    url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="links")


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    image_url_full_1 = Column(String, nullable=False)
    image_url_display_1 = Column(String, nullable=False)
    image_url_full_2 = Column(String, nullable=False)
    image_url_display_2 = Column(String, nullable=False)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = relationship("User", back_populates="posts")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(String, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="reset_tokens")
