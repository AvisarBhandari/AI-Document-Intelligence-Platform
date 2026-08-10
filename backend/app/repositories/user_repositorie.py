from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    @staticmethod
    def get_user_by_email(db:Session, email:str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate, hashed_pass: str):
        db_user = User(
            email = user_data.email,
            username = user_data.username,
            hashed_password = hashed_pass
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user