from app.core.database import get_db
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserRegisterSuccessResponse,
)
from app.services.auth_services import AuthService
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    login_credentials = UserLogin(email=form_data.username, password=form_data.password)
    token = AuthService.login(db, login_credentials)
    return {
        "status": "success",
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
    }


@router.post(
    "/register",
    response_model=UserRegisterSuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = AuthService.register(db, user_data)
    return {
        "status": "success",
        "message": "User account created successfully!",
        "data": new_user,
    }
