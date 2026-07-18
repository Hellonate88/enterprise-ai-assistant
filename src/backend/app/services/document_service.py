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


from pathlib import Path

from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository

from app.models.document import Document


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
    
    def get_all_documents(self):
        return self.repository.get_all()
    
    def delete_document(self, document_id: int):

        #storage 文件夹删除
        document = self.repository.get_by_id(document_id)
        if document and document.filepath:
            file_path = Path(document.filepath)
            if file_path.exists():
                file_path.unlink()  # Delete the file from the filesystem

        #数据库真正删除
        self.repository.delete(document_id)
    
    def get_document(self, document_id: int) -> Document | None:
        document = self.repository.get_by_id(document_id)

        if document is None:

            raise ValueError(
                "Document not found"
            )

        return document



