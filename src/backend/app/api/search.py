from pytest import Session
from fastapi import APIRouter, Depends
from backend.app.repositories.embedding_repository import EmbeddingRepository
from backend.app.schemas.search import SearchRequest
from backend.app.services.embedding.fake_embedding_provider import FakeEmbeddingProvider
from backend.app.services.embedding_service import EmbeddingService
from backend.app.services.retrieval_service import RetrievalService
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/")
def search_documents(
    request: SearchRequest,
    db: Session = Depends(get_db)
):

    provider = FakeEmbeddingProvider()

    embedding_service = EmbeddingService(provider)

    embedding_repository = EmbeddingRepository(db)

    retrieval_service = RetrievalService(
        embedding_service,
        embedding_repository
    )

    return retrieval_service.retrieve(
        query=request.query,
        top_k=request.top_k
    )