from app.core.database import SessionLocal

from app.repositories.chunk_repository import ChunkRepository
from app.repositories.embedding_repository import (
    EmbeddingRepository
)
from app.services.embedding_service import EmbeddingService
from app.services.reindex_service import ReindexService


def main():

    db = SessionLocal()

    try:

        chunk_repository = ChunkRepository(db)

        embedding_repository = EmbeddingRepository(db)

        embedding_service = EmbeddingService()

        reindex_service = ReindexService(
            chunk_repository=chunk_repository,
            embedding_repository=embedding_repository,
            embedding_service=embedding_service
        )

        result = reindex_service.reindex_all()

        print(result)

    finally:

        db.close()


if __name__ == "__main__":
    main()