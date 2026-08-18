import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    PROJECT_NAME: str = "AI Document Intelligence Platform"
    DATABASE_URL: str = os.getenv("DATABASE_URL") or os.getenv("URL_DATABASE")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))

settings = Settings()