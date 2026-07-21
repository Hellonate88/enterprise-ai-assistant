from pathlib import Path
import logging

from pypdf import PdfReader

logger = logging.getLogger(__name__)


class TextExtractionService:

    def extract_text(self, file_path: str) -> str:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return self._extract_pdf(path)

        if suffix == ".txt":
            return self._extract_txt(path)

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    def _extract_pdf(self, path: Path) -> str:

        logger.info(f"Extracting PDF: {path.name}")

        reader = PdfReader(path)

        text_parts = []

        for page_number, page in enumerate(reader.pages, start=1):

            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

            else:
                logger.warning(
                    f"Page {page_number} has no extractable text"
                )

        full_text = "\n".join(text_parts)

        logger.info(
            f"Extracted {len(full_text)} characters from PDF"
        )

        return full_text

    def _extract_txt(self, path: Path) -> str:

        logger.info(f"Extracting TXT: {path.name}")

        text = path.read_text(
            encoding="utf-8"
        )

        logger.info(
            f"Extracted {len(text)} characters from TXT"
        )

        return text