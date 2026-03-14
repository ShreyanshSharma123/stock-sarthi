"""
Pydantic schemas for User-related API requests/responses
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for user information"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserResponse(UserBase):
    """Response schema for user data"""
    id: int
    full_name: Optional[str]
    is_active: bool
    is_premium: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload"""
    user_id: Optional[int] = None
