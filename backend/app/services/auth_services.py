from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user import UserCreate, UserLogin
from app.repositories.user_repositorie import UserRepository
from app.core.security import SecurityUtils
from app.dependencies.auth import JWTManager
from app.models.user import User

class AuthService:
    @staticmethod
    def register(db: Session, user_data: UserCreate) -> User:
        # Check if user exists
        existing_user = UserRepository.get_user_by_email(db=db, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        # Example using a dummy placeholder hash :
        # hashed_password = f"secure_hash_{user_data.password}"
        # Real secure bcrypt hashing
        hashed_password = SecurityUtils.has_password(user_data.password)
        return UserRepository.create_user(db, user_data, hashed_password)

    @staticmethod
    def login(db: Session, login_data: UserLogin) -> str:
        user = UserRepository.get_user_by_email(db, login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        if not SecurityUtils.verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        return JWTManager.create_access_token(data={"sub": str(user.id)})