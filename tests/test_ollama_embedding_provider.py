from app.services.embedding.ollama_embedding_provider import (
    OllamaEmbeddingProvider
)


def test_ollama_embedding_provider():

    provider = OllamaEmbeddingProvider(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )

    embedding = provider.generate_embedding(
        "Employees receive 20 days of annual leave."
    )

    print(len(embedding))

    assert isinstance(embedding, list)

    assert len(embedding) > 0

    assert isinstance(
        embedding[0],
        float
    )