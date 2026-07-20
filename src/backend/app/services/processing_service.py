import time
import logging

from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.models.document_status import DocumentStatus

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
            self.repository.update_status(
                document_id,
                DocumentStatus.READY
            )

            logger.info(f"Document {document_id} is READY")
