import os
import uuid

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.document_service import DocumentService
from app.schemas.document import (DocumentResponse, DocumentUploadResponse, DocumentListResponse)
from app.repositories.document_repository import DocumentRepository

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    response_model=DocumentUploadResponse
):
    # Read the uploaded file 
    file_cuntent = await file.read()

    # Get file size in bytes
    file_size = len(file_cuntent)

    # Validate the uploaded file
    DocumentService.validate_file(
        file_type=file.content_type,
        file_size=file_size,
    )

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]

    unique_filename = f"{uuid.uuid4()}{file_extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    # Save the file 
    with open(file_path, "wb") as buffer:
        buffer.write(file_cuntent)

    # Create database record
    document = DocumentService.create_document(
        db= db,
        user_id= current_user.id,
        filename= unique_filename,
        original_filename= file.filename,
        file_path= file_path,
        file_type= file.content_type,
        file_size= file_size,
    )

    return {
        "status": "success",
        "message": "Document uploaded successfull",
        "data": document,
    }    


@router.get("", response_model=DocumentListResponse)
async def get_user_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = DocumentService.get_user_documents(
        db = db,
        user_id = current_user.id
    )
    return {
        "status": "success",
        "message": "Documents retrieved successfully",
        "data": documents,
    }


@router.get(
    "/{document_id}",
    response_model=DocumentResponse
)
async def get_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> DocumentResponse:
    document = DocumentService.get_document_by_id(
        db=db,
        document_id=document_id,
        user_id=current_user.id
    )
    return document