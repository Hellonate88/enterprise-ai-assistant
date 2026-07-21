from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk

class ChunkRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_chunks(
        self,
        document_id: int,
        chunks: list[str]
    ):

        for index, chunk_text in enumerate(chunks):

            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=chunk_text,
                char_count=len(chunk_text)
            )

            self.db.add(chunk)

        self.db.commit()