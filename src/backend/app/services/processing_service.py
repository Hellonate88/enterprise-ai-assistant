import time
import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.models.document_status import DocumentStatus
from app.services.text_extraction_service import TextExtractionService
from app.repositories.chunk_repository import ChunkRepository
from app.services.chunking_service import ChunkingService

logger = logging.getLogger(__name__)

class ProcessingService:

    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    def process_document(self, document_id: int):

        logger.info(f"Start processing document {document_id}")

        # 1. 更新为 PROCESSING
        self.repository.update_status(
            document_id,
            DocumentStatus.PROCESSING
        )

        # 2. 模拟耗时 AI 任务
        time.sleep(3)

        document = self.repository.get_by_id(document_id)

        if "fail" in document.filename.lower():
            self.repository.update_status(
                document_id,
                DocumentStatus.FAILED
            )

            logger.info(f"Document {document_id} is FAILED")

        else:
            text = TextExtractionService().extract_text(
                document.filepath
            )

            self.repository.update_raw_text(
                document_id,
                text
            )

            # Chunk
            chunks = ChunkingService().split_text(text)

            # save Chunk
            ChunkRepository(self.repository.db).create_chunks(
                document.id,
                chunks
            )

            self.repository.update_status(
                document_id,
                DocumentStatus.READY
            )

            logger.info(f"Document {document_id} is READY")
