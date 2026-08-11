from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    UserCreate, UserRegisterSuccessResponse,
    UserLogin, TokenResponse, UserResponse
    )
from app.services.auth_services import AuthService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    token = AuthService.login(db, login_data)
    return{"status": "success", 
           "message": "Login successful",
           "access_token": token,
           "token_type": "bearer"}

@router.post("/register", response_model=UserRegisterSuccessResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db:Session = Depends(get_db)):

    new_user= AuthService.register(db, user_data)
    return{
        "status": "success",
        "message": "User account created successfully!",
        "data": new_user
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user