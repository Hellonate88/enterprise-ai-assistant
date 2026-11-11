from src.backend.app.services.chunking_service import ChunkingService


def test_split_text_stops_after_final_chunk_with_overlap():
    text = "a" * 990 + ". " + "b" * 721 + ". c"

    chunks = ChunkingService().split_text(text)

    assert len(chunks) == 3
    assert chunks[-1].endswith("c")
