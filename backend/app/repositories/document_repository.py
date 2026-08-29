from pydoc import Doc
import uuid

from app.models.document import Document
from sqlalchemy.orm import Session


class DocumentRepository:
    @staticmethod
    def create_document(
        db: Session,
        user_id: uuid.UUID,
        filename: str,
        original_filename: str,
        file_path: str,
        file_type: str,
        file_size: int,
    ) -> Document:
        document = Document(
            user_id=user_id,
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            status="uploaded",
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def get_documents_by_user(
        db: Session,
        user_id: uuid.UUID,
    ) -> list[Document]:
        return (
            db.query(Document)
            .filter(Document.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_document_by_id(
        db: Session,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Document | None:
        return (
            db.query(Document)
            .filter(
                Document.id == document_id,
                Document.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def delete_document(
        db: Session,
        document_id: uuid.UUID,
        user_id: uuid.UUID
    ) -> Document | None:
        document = (
            db.query(Document)
            .filter(
                Document.id == document_id,
                Document.user_id == user_id
            )
            .first()
        )
        if not document:
            return None
        db.delete(document)
        db.commit()

        return document

