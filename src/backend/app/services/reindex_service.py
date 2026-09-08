from app.repositories.chunk_repository import ChunkRepository
from app.repositories.embedding_repository import (
    EmbeddingRepository
)
from app.services.embedding_service import EmbeddingService


class ReindexService:

    def __init__(
        self,
        chunk_repository: ChunkRepository,
        embedding_repository: EmbeddingRepository,
        embedding_service: EmbeddingService
    ):
        self.chunk_repository = chunk_repository
        self.embedding_repository = embedding_repository
        self.embedding_service = embedding_service

    def reindex_all(self) -> dict:

        # Step 1: Get all chunks
        chunks = self.chunk_repository.get_all()

        # Step 2: Delete old embeddings
        deleted_count = (
            self.embedding_repository.delete_all()
        )

        # Step 3: Generate new embeddings
        created_count = 0
        dimension = None

        for chunk in chunks:

            vector = (
                self.embedding_service.generate_embedding(
                    chunk.content
                )
            )

            # Save dimension from generated vector
            dimension = len(vector)

            self.embedding_repository.create(
                chunk_id=chunk.id,
                model=self.embedding_service.model_name,
                vector=vector
            )

            created_count += 1

        # Step 4: Return summary
        return {
            "chunks_processed": len(chunks),
            "embeddings_deleted": deleted_count,
            "embeddings_created": created_count,
            "model": self.embedding_service.model_name,
            "dimension": dimension
        }