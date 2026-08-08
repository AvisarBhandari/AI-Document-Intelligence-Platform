from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import date
class UserBase(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid42)
    email: EmailStr
    name: str
    hashed_password: str
    is_active: bool
    is_vetified: bool
    created_at: date
    updated_at: date
    profile_picture: str

