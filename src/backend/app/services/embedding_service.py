import hashlib
import math
import os
import ssl

import httpx
from openai import OpenAI


class FakeEmbeddingProvider:
    """Deterministic embedding provider for development / testing.

    * Same text  → always the same vector.
    * Different texts → different vectors.
    * No network calls, no API key required.

    Strategy
    --------
    1. Hash the text with SHA-256 to get a 32-byte seed.
    2. Extend the seed to `DIM` floats by repeatedly hashing
       (seed + chunk_index) – fully deterministic, no randomness.
    3. Normalise the vector to unit length so it behaves like a
       real embedding (cosine similarity works out of the box).
    """

    DIM = 1536  # matches text-embedding-3-small output dimension

    def generate_embedding(self, text: str) -> list[float]:
        seed = hashlib.sha256(text.encode("utf-8")).digest()  # 32 bytes

        raw: list[float] = []
        chunk = 0
        while len(raw) < self.DIM:
            block = hashlib.sha256(seed + chunk.to_bytes(4, "big")).digest()
            # Each byte → value in [-1, 1]
            for byte in block:
                raw.append((byte - 127.5) / 127.5)
                if len(raw) == self.DIM:
                    break
            chunk += 1

        # Normalise to unit vector
        magnitude = math.sqrt(sum(v * v for v in raw))
        if magnitude == 0:
            return raw  # extremely unlikely, but safe
        return [v / magnitude for v in raw]


class EmbeddingService:

    MODEL = "text-embedding-3-small"

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