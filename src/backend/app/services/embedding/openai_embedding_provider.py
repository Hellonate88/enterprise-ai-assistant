import os
import ssl

import httpx
from openai import OpenAI

from .embedding_provider import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """Real embedding provider using OpenAI API."""

    MODEL = "text-embedding-3-small"

    @property
    def model_name(self) -> str:
        return self.MODEL

    @staticmethod
    def _build_client() -> OpenAI:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_ADMIN_KEY")

        if not api_key:
            raise RuntimeError(
                "Missing OpenAI credentials. Set OPENAI_API_KEY (or OPENAI_ADMIN_KEY) before generating embeddings."
            )

        ca_bundle = (
            os.getenv("OPENAI_CA_BUNDLE")
            or os.getenv("SSL_CERT_FILE")
            or os.getenv("REQUESTS_CA_BUNDLE")
        )

        if ca_bundle:
            http_client = httpx.Client(verify=ca_bundle)
        else:
            http_client = httpx.Client(verify=ssl.create_default_context())

        return OpenAI(
            api_key=api_key,
            http_client=http_client
        )

    def generate_embedding(self, text: str) -> list[float]:
        client = self._build_client()

        try:
            response = client.embeddings.create(
                model=self.MODEL,
                input=text
            )

            return response.data[0].embedding

        finally:
            client.close()
