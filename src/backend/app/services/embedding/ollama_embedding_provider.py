from ollama import Client

from app.services.embedding.embedding_provider import (
    EmbeddingProvider
)


class OllamaEmbeddingProvider(EmbeddingProvider):

    def __init__(
        self,
        model: str,
        base_url: str
    ):
        self.model = model

        self.client = Client(
            host=base_url
        )

    @property
    def model_name(self) -> str:
        return self.model

    def generate_embedding(
        self,
        text: str
    ) -> list[float]:

        response = self.client.embed(
            model=self.model,
            input=text
        )

        return response["embeddings"][0]