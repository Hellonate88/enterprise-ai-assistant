from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_status import DocumentStatus

from pathlib import Path

class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        filename: str,
        filepath: str,
        status: str
    ) -> Document:

        document = Document(
            filename=filename,
            filepath=filepath,
            status=status
        )

        self.db.add(document)

        self.db.commit()

        self.db.refresh(document)

        return document

    def get_all(self) -> list[Document]:
        return (
            self.db.query(Document)
            .order_by(Document.id.desc())
            .all()
        )
    
    def delete(self, document_id: int):
        document = self.db.query(Document).filter(Document.id == document_id).first()

        if document:
            self.db.delete(document)
            self.db.commit()
    
    def get_by_id(self, document_id: int) -> Document | None:
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def update_status(
        self,
        document_id: int,
        status: DocumentStatus
    ):

        document = self.get_by_id(document_id)

        if document is None:
            return None

        document.status = status

        self.db.commit()

        self.db.refresh(document)

        return document

