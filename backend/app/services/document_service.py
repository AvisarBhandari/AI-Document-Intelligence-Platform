import uuid

from app.repositories.document_repository import DocumentRepository
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

ALLOWED_FILE_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class DocumentService:
    @staticmethod
    def validate_file(
        file_type: str,
        file_size: int,
    ) -> None:

        # Validate file type
        if file_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type"
            )

        # Validate file size
        if file_size <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="File cannot be empty"
            )

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds the 10 MB limit",
            )

    @staticmethod
    def create_document(
        db: Session,
        user_id: uuid.UUID,
        filename: str,
        original_filename: str,
        file_path: str,
        file_type: str,
        file_size: int,
    ):
        DocumentService.validate_file(
            file_type=file_type,
            file_size=file_size,
        )

        document = DocumentRepository.create_document(
            db=db,
            user_id=user_id,
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
        )

        return document
