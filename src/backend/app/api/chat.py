from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories.embedding_repository import EmbeddingRepository
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.embedding.fake_embedding_provider import FakeEmbeddingProvider
from app.services.embedding_service import EmbeddingService
from app.services.llm.fake_llm_provider import FakeLLMProvider
from app.services.llm.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.services.llm.llm_provider_factory import LLMProviderFactory

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post(
    "",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    embedding_provider = FakeEmbeddingProvider()

    embedding_service = EmbeddingService(
        embedding_provider
    )

    embedding_repository = EmbeddingRepository(db)
    
    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        embedding_repository=embedding_repository
    )

    llm_provider = LLMProviderFactory.create()
    llm_service = LLMService(llm_provider)

    chat_service = ChatService(
        retrieval_service=retrieval_service,
        llm_service=llm_service
    )

    try:
        return chat_service.ask(
            question=request.question,
            top_k=request.top_k
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail="AI Provider currently unavailable. "
                   "Please ensure all services are running."
        ) from e