from .embedding import EmbeddingProvider, OpenAIEmbeddingProvider


class EmbeddingService:
    """Wrapper around EmbeddingProvider.

    Allows dependency injection for flexibility — swap between
    OpenAIEmbeddingProvider (production) and FakeEmbeddingProvider (testing).
    """

    def __init__(self, provider: EmbeddingProvider | None = None):
        """Initialize with a provider.

        Args:
            provider: EmbeddingProvider instance.
                     Defaults to OpenAIEmbeddingProvider if None.
        """
        self.provider = provider or OpenAIEmbeddingProvider()

    def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for the given text."""
        return self.provider.generate_embedding(text)