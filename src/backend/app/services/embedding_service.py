from app.services.embedding.embedding_provider import EmbeddingProvider
from app.services.embedding.embedding_provider_factory import (
    EmbeddingProviderFactory
)


class EmbeddingService:

    def __init__(
        self,
        provider: EmbeddingProvider | None = None
    ):
        self.provider = (
            provider
            if provider is not None
            else EmbeddingProviderFactory.create()
        )

    def generate_embedding(
        self,
        text: str
    ) -> list[float]:

        return self.provider.generate_embedding(text)

    @property
    def model_name(self) -> str:

        return self.provider.model_name