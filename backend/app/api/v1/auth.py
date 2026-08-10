from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserRegisterSuccessResponse
from app.services.auth_services import AuthService

router = APIRouter()

@router.get("/login")
async def login():
    # Next step: implement token generation here
    return("Login Successfull")

@router.post("/register", response_model=UserRegisterSuccessResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db:Session = Depends(get_db)):

    new_user= AuthService.register(db, user_data)
    return{
        "status": "success",
        "message": "User account created successfully!",
        "data": new_user
    }