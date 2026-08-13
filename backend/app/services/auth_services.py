from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user import UserCreate, UserLogin
from app.repositories.user_repository import UserRepository
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
                detail={"status": "fail",
                        "error_code": "EMAIL_ALREADY-EXISTS",
                        "message": f"The email address '{user_data.email}' is already registered to an account.",
                        "field": "email"
                        }
            )
        # Example using a dummy placeholder hash :
        # hashed_password = f"secure_hash_{user_data.password}"
        # Real secure bcrypt hashing
        hashed_password = SecurityUtils.hash_password(user_data.password)
        return UserRepository.create_user(db, user_data, hashed_password)

    @staticmethod
    def login(db: Session, login_data: UserLogin) -> str:
        # Fetch the user data from database
        user = UserRepository.get_user_by_email(db, login_data.email)
        # Security Note: We use the exact same error object structure for both missing user 
        # and bad passwords to prevent malicious enumeration attacks.
        auth_failed_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "fail",
                "error_code": "INVALID_CREDENTIALS",
                "message": "The email address or password you entered is incorrect."
            }
        )
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