from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime

# shared fields across schemas 
class UserBase(BaseModel):
    email:EmailStr
    username: str
# Schema used for user registration input
class UserCreate(UserBase):
    password: str
# Schema used for API responses
class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    profile_picture: str | None = None

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models

class UserRegisterSuccessResponse(BaseModel):
    status: str = "success"
    message: str = "User registered successfully"
    data: UserResponse # This embeds existing user response fields

# for login and register
class UserLogin(BaseModel):
    email:EmailStr
    password: str

class TokenResponse(BaseModel):
    status: str = "success"
    message: str = "Login successfull" 
    access_token: str
    token_type: str = "bearer"