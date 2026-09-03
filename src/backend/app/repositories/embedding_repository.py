from sqlalchemy.orm import Session

from ..models.chunk_embedding import ChunkEmbedding

class EmbeddingRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        chunk_id: int,
        model: str,
        vector: list[float]
    ) -> ChunkEmbedding:

        embedding = ChunkEmbedding(
            chunk_id=chunk_id,
            model=model,
            vector_json=vector,
            dimension=len(vector)
        )

        self.db.add(embedding)

        self.db.commit()

        self.db.refresh(embedding)

        return embedding

    def get_by_chunk_id(
        self,
        chunk_id: int
    ) -> ChunkEmbedding | None:

        return (
            self.db.query(ChunkEmbedding)
            .filter(ChunkEmbedding.chunk_id == chunk_id)
            .first()
        )

    def get_all_embeddings(self):
        return self.db.query(ChunkEmbedding).all()