import time
import logging

from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.embedding_repository import EmbeddingRepository

from app.models.document_status import DocumentStatus

from app.services.text_extraction_service import TextExtractionService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from  app.services.embedding_service import FakeEmbeddingProvider

logger = logging.getLogger(__name__)

class ProcessingService:

    def __init__(self, db: Session):
        self.db = db
        self.document_repository = DocumentRepository(db)
        self.chunk_repository = ChunkRepository(db)
        self.embedding_repository = EmbeddingRepository(db)

    def process_document(self, document_id: int):

        try:

            document = self.document_repository.get_by_id(document_id)

            if document is None:
                logger.error(f"Document {document_id} not found")
                return

            # 1. PROCESSING
            self.document_repository.update_status(
                document.id,
                DocumentStatus.PROCESSING
            )

            # 2. 提取文本
            text = TextExtractionService().extract_text(
                document.filepath
            )

            # 3. 保存原始文本
            self.document_repository.update_raw_text(
                document.id,
                text
            )

            # 4. Chunk
            chunks = ChunkingService().split_text(text)

            # 5. 保存 Chunk
            chunk_entities = self.chunk_repository.create_chunks(
                document.id,
                chunks
            )

            # 6. 生成 Embedding
            ##embedding_service = EmbeddingService()
            embedding_service = FakeEmbeddingProvider()

            for chunk in chunk_entities:

                # 缓存检查（Challenge）
                existing = self.embedding_repository.get_by_chunk_id(
                    chunk.id
                )

                if existing:
                    logger.info(
                        f"Embedding already exists for chunk {chunk.id}"
                    )
                    continue

                vector = embedding_service.generate_embedding(
                    chunk.content
                )

                self.embedding_repository.create(
                    chunk_id=chunk.id,
                    model=FakeEmbeddingProvider.DIM, ##model=EmbeddingService.MODEL,
                    vector=vector
                )

            # 7. READY
            self.document_repository.update_status(
                document.id,
                DocumentStatus.READY
            )

            logger.info(
                f"Document {document_id} processed successfully"
            )

        except Exception as e:

            logger.exception(
                f"Processing failed for document {document_id}: {e}"
            )

            document = self.document_repository.get_by_id(document_id)

            if document:
                self.document_repository.update_status(
                    document.id,
                    DocumentStatus.FAILED
                )