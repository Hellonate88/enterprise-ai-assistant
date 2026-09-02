import pytest
from src.backend.app.services.embedding import FakeEmbeddingProvider
from src.backend.app.services.embedding_service import EmbeddingService


class TestEmbeddingService:
    """Test suite for EmbeddingService with different providers."""

    @pytest.fixture
    def fake_service(self):
        """Create EmbeddingService with FakeEmbeddingProvider."""
        provider = FakeEmbeddingProvider()
        return EmbeddingService(provider=provider)

    def test_same_text_same_embedding(self, fake_service):
        """Test 1: Same text produces same embedding (deterministic)."""
        text = "The quick brown fox jumps over the lazy dog"

        embedding_1 = fake_service.generate_embedding(text)
        embedding_2 = fake_service.generate_embedding(text)

        # Same text should produce exactly the same vector
        assert embedding_1 == embedding_2, \
            "Same text should produce identical embeddings"

    def test_different_texts_different_embeddings(self, fake_service):
        """Test 2: Different texts produce different embeddings."""
        text_1 = "Hello world"
        text_2 = "Goodbye world"

        embedding_1 = fake_service.generate_embedding(text_1)
        embedding_2 = fake_service.generate_embedding(text_2)

        # Different texts should produce different vectors
        assert embedding_1 != embedding_2, \
            "Different texts should produce different embeddings"

    def test_embedding_dimension(self, fake_service):
        """Test 3: Embedding has correct dimension (1536)."""
        text = "Test text"
        embedding = fake_service.generate_embedding(text)

        assert len(embedding) == 1536, \
            f"Expected dimension 1536, got {len(embedding)}"

    def test_embedding_is_normalized(self, fake_service):
        """Test 4: Embedding is unit-normalized (L2 norm ≈ 1)."""
        import math

        text = "Normalize me"
        embedding = fake_service.generate_embedding(text)

        magnitude = math.sqrt(sum(v * v for v in embedding))

        assert abs(magnitude - 1.0) < 1e-6, \
            f"Expected unit norm, got {magnitude}"

    def test_provider_model_name(self, fake_service):
        """Test 5: Provider exposes correct model name."""
        assert fake_service.provider.model_name == "fake-embedding", \
            "FakeEmbeddingProvider should have model_name='fake-embedding'"
