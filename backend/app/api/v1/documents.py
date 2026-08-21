from fastapi import APIRouter, Depends
from requests import Session
from app.dependencies.auth import get_current_user
from backend.app.core.database import get_db


router = APIRouter()


@router.post("/upload", status_code=202)
async def upload_document(current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    return("Upload","TEST")