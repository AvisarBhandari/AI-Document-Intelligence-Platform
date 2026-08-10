from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repositorie import UserRepository
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
        # TODO: Implement real password hashing here!!!
        # 3xample using a dummy placeholder hash for now :
        hashed_password = f"secure_hash_{user_data.password}"

        return UserRepository.create_user(db, user_data, hashed_password)