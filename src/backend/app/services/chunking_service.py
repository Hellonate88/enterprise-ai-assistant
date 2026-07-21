class ChunkingService:

    def split_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> list[str]:

        if not text:
            return []

        chunks = []

        start = 0

        text_length = len(text)

        while start < text_length:

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            # 下一块从 overlap 之前开始
            start += chunk_size - overlap

        return chunks