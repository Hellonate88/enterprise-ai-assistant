from app.services.embedding.embedding_provider import (
    EmbeddingProvider
)
from app.core.config import settings

from app.services.embedding.fake_embedding_provider import (
    FakeEmbeddingProvider
)

from app.services.embedding.ollama_embedding_provider import (
    OllamaEmbeddingProvider
)


class EmbeddingProviderFactory:

    @staticmethod
    def create() -> EmbeddingProvider:

        if settings.embedding_provider == "fake":

            return FakeEmbeddingProvider()

        if settings.embedding_provider == "ollama":

            return OllamaEmbeddingProvider(
                model=settings.ollama_embedding_model,
                base_url=settings.ollama_base_url
            )

        raise ValueError(
            f"Unsupported embedding provider: "
            f"{settings.embedding_provider}"
        )