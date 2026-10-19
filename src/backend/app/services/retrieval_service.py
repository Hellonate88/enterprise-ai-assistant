import math
from .embedding_service import EmbeddingService
from ..repositories.embedding_repository import EmbeddingRepository


class RetrievalService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        embedding_repository: EmbeddingRepository
    ):
        self.embedding_service = embedding_service
        self.embedding_repository = embedding_repository

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.0
    ):
        """Retrieve top K most similar chunks for a query.

        Steps:
        1. Generate Query Embedding
        2. Get All Stored Embeddings
        3. Calculate Similarity
        4. Filter by Threshold
        5. Build Results
        6. Sort Results
        7. Return Top K

        Args:
            query: Query text
            top_k: Number of results to return (default: 5)
            score_threshold: Minimum similarity score to include (default: 0.0)

        Returns:
            List of dicts with keys:
            - chunk_id: ID of the chunk
            - document_id: ID of the document
            - content: Text content of the chunk
            - score: Cosine similarity score (0-1)

        Raises:
            ValueError: If top_k <= 0
        """

        # Validate top_k parameter
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        # Step 1: Generate Query Embedding
        query_embedding = (
            self.embedding_service.generate_embedding(query)
        )

        # Step 2: Get All Stored Embeddings by model name
        current_model = (
            self.embedding_service.model_name
        )

        embeddings = (
            self.embedding_repository.get_embeddings_by_model(
                current_model
    )
)

        # Handle empty embeddings gracefully
        if not embeddings:
            return []

        # Step 3, 4 & 5: Calculate Similarity, Filter by Threshold, Build Results
        results = []
        for embedding in embeddings:
            stored_vector = embedding.vector_json
            
            score = cosine_similarity(
                query_embedding,
                stored_vector
            )

            # Filter by score threshold
            if score >= score_threshold:
                result = {
                    "chunk_id": embedding.chunk.id,
                    "document_id": embedding.chunk.document_id,
                    "filename": embedding.chunk.document.filename,
                    "content": embedding.chunk.content,
                    "score": score
                }
                results.append(result)

        # Step 6: Sort by score (descending)
        results.sort(key=lambda x: x["score"], reverse=True)

        # Step 7: Return Top K
        return results[:top_k]


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float]
) -> float:

    if len(vector_a) != len(vector_b):
        raise ValueError(
            f"Vectors must have the same dimensions. "
            f"Got {len(vector_a)} and {len(vector_b)}"
        )

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )