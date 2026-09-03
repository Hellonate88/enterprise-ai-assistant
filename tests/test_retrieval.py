import sys
import os

# Add backend to path
backend_path = os.path.join(
    os.path.dirname(__file__), 
    "..", 
    "src", 
    "backend"
)
sys.path.insert(0, backend_path)

from src.backend.app.services.retrieval_service import cosine_similarity, RetrievalService
from src.backend.app.services.embedding_service import EmbeddingService
from src.backend.app.services.embedding import FakeEmbeddingProvider
from unittest.mock import Mock, MagicMock


def test_identical_vectors():
    """Test that identical vectors have cosine similarity of 1.0."""
    vector_a = [1.0, 0.0, 0.0]
    vector_b = [1.0, 0.0, 0.0]

    score = cosine_similarity(
        vector_a,
        vector_b
    )

    assert score == 1.0


def test_orthogonal_vectors():
    """Test that orthogonal vectors have cosine similarity of 0.0."""
    vector_a = [1.0, 0.0, 0.0]
    vector_b = [0.0, 1.0, 0.0]

    score = cosine_similarity(
        vector_a,
        vector_b
    )

    assert score == 0.0


def test_opposite_vectors():
    """Test that opposite vectors have cosine similarity of -1.0."""
    vector_a = [1.0, 0.0, 0.0]
    vector_b = [-1.0, 0.0, 0.0]

    score = cosine_similarity(
        vector_a,
        vector_b
    )

    assert score == -1.0


def test_retrieve_returns_top_k():
    """Test that retrieve() returns top K results sorted by score."""
    # Setup mock embedding service
    embedding_service = EmbeddingService(provider=FakeEmbeddingProvider())

    # Setup mock embedding repository
    embedding_repo = Mock()

    # Create mock chunks with id and document_id
    chunk_1 = Mock()
    chunk_1.id = 1
    chunk_1.document_id = 10
    chunk_1.content = "The quick brown fox"

    chunk_2 = Mock()
    chunk_2.id = 2
    chunk_2.document_id = 10
    chunk_2.content = "The lazy dog"

    chunk_3 = Mock()
    chunk_3.id = 3
    chunk_3.document_id = 20
    chunk_3.content = "Python is awesome"

    # Create mock embeddings
    embedding_1 = Mock()
    embedding_1.chunk = chunk_1
    embedding_1.vector_json = [0.1, 0.2, 0.3, 0.4, 0.5] * 307 + [0.1]  # 1536 dims

    embedding_2 = Mock()
    embedding_2.chunk = chunk_2
    embedding_2.vector_json = [0.2, 0.3, 0.4, 0.5, 0.1] * 307 + [0.2]  # Different

    embedding_3 = Mock()
    embedding_3.chunk = chunk_3
    embedding_3.vector_json = [0.5, 0.1, 0.2, 0.3, 0.4] * 307 + [0.5]  # Different

    embedding_repo.get_all_embeddings.return_value = [
        embedding_1,
        embedding_2,
        embedding_3
    ]

    # Create retrieval service
    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        embedding_repository=embedding_repo
    )

    # Perform retrieval
    results = retrieval_service.retrieve(query="quick fox", top_k=2)

    # Verify
    assert len(results) == 2, "Should return 2 results (top_k=2)"
    
    # Verify each result has required fields
    for result in results:
        assert "chunk_id" in result, "Each result should have chunk_id"
        assert "document_id" in result, "Each result should have document_id"
        assert "content" in result, "Each result should have content"
        assert "score" in result, "Each result should have score"

    # Verify results are sorted by score (descending)
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True), \
        "Results should be sorted by score in descending order"
    
    # Verify chunk_id and document_id are correctly set
    assert results[0]["chunk_id"] in [1, 2, 3]
    assert results[0]["document_id"] in [10, 20]
    
    print("\n✅ Retrieve Test Passed!")
    print(f"   Top result: {results[0]['content']} (score: {results[0]['score']:.4f})")
    if len(results) > 1:
        print(f"   Second result: {results[1]['content']} (score: {results[1]['score']:.4f})")


def test_retrieve_empty_embeddings():
    """Test that retrieve() returns empty list when no embeddings exist."""
    # Setup mock embedding service
    embedding_service = EmbeddingService(provider=FakeEmbeddingProvider())

    # Setup mock embedding repository
    embedding_repo = Mock()
    embedding_repo.get_all_embeddings.return_value = []  # Empty database

    # Create retrieval service
    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        embedding_repository=embedding_repo
    )

    # Perform retrieval on empty database
    results = retrieval_service.retrieve(query="any query", top_k=5)

    # Verify it returns empty list, not error
    assert isinstance(results, list), "Results should be a list"
    assert len(results) == 0, "Should return empty list for empty database"
    
    print("\n✅ Empty Database Test Passed!")
    print("   Returned: []")


def test_retrieve_invalid_top_k():
    """Test that retrieve() raises ValueError for invalid top_k values."""
    # Setup mock services
    embedding_service = EmbeddingService(provider=FakeEmbeddingProvider())
    embedding_repo = Mock()
    embedding_repo.get_all_embeddings.return_value = []

    # Create retrieval service
    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        embedding_repository=embedding_repo
    )

    # Test top_k = 0
    try:
        retrieval_service.retrieve(query="test", top_k=0)
        assert False, "Should raise ValueError for top_k=0"
    except ValueError as e:
        assert str(e) == "top_k must be greater than 0"
        print("\n✅ top_k=0 Validation Test Passed!")
        print(f"   Error: {e}")

    # Test top_k = -1
    try:
        retrieval_service.retrieve(query="test", top_k=-1)
        assert False, "Should raise ValueError for top_k=-1"
    except ValueError as e:
        assert str(e) == "top_k must be greater than 0"
        print("\n✅ top_k=-1 Validation Test Passed!")
        print(f"   Error: {e}")