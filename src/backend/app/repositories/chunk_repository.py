from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk

class ChunkRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_chunks(
        self,
        document_id: int,
        chunks: list[str]
    ) -> list[DocumentChunk]:

        chunk_entities = []

        for index, chunk_text in enumerate(chunks):

            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=chunk_text,
                char_count=len(chunk_text)
            )

            self.db.add(chunk)

            chunk_entities.append(chunk)

        # 一次性提交
        self.db.commit()

        # 刷新，拿到自动生成的 id
        for chunk in chunk_entities:
            self.db.refresh(chunk)

        return chunk_entities

    def get_all(self) -> list[DocumentChunk]:

        return (
            self.db.query(DocumentChunk)
            .order_by(
                DocumentChunk.document_id,
                DocumentChunk.chunk_index
            )
            .all()
        )