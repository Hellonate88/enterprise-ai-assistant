from pydantic import BaseModel


class ChatRequest(BaseModel):

    question: str

    top_k: int = 3


class SourceResponse(BaseModel):
    """Schema for a single source document chunk."""

    document_id: int

    chunk_id: int

    filename: str

    content: str

    score: float


class ChatResponse(BaseModel):
    """Schema for chat API response with answer and sources."""

    answer: str

    sources: list[SourceResponse]