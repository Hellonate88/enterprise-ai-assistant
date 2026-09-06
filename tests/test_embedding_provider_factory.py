from app.services.embedding.embedding_provider_factory import (
    EmbeddingProviderFactory
)

from app.services.embedding.ollama_embedding_provider import (
    OllamaEmbeddingProvider
)


def test_factory_creates_ollama_embedding_provider():

    provider = EmbeddingProviderFactory.create()

    assert isinstance(
        provider,
        OllamaEmbeddingProvider
    )