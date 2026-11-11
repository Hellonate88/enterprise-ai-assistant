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

            target_end = min(start + chunk_size, text_length)

            # 默认结束位置
            end = target_end

            # 在目标结束位置附近寻找更好的句子边界
            search_window = text[start:target_end]

            boundary_candidates = [
                search_window.rfind(". "),
                search_window.rfind("\n"),
                search_window.rfind("。"),
                search_window.rfind("! "),
                search_window.rfind("? ")
            ]

            best_boundary = max(boundary_candidates)

            # 只有在距离末尾不太远时才使用句子边界
            if best_boundary != -1 and best_boundary > chunk_size * 0.6:
                end = start + best_boundary + 1

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            # 计算下一块起点（保留 overlap）
            next_start = max(end - overlap, start + 1)

            start = next_start

        return chunks