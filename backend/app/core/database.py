from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("URL_DATABASE")
engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

# Helper function to yield database sessions to endpoints


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        