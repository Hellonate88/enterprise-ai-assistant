# from app.models.document import Document

# def create_document(db, filename, filepath, status):
#     document = Document(
#         filename=filename,
#         filepath=filepath,
#         status=status
#     )
#     db.add(document)
#     db.commit()
#     db.refresh(document)
#     return document


from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository


class DocumentService:

    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    def upload_document(
        self,
        filename: str,
        filepath: str
    ):

        document = self.repository.create(
            filename=filename,
            filepath=filepath,
            status="UPLOADED"
        )

        return document