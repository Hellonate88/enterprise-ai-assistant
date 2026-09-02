import hashlib
import math

from .embedding_provider import EmbeddingProvider


class FakeEmbeddingProvider(EmbeddingProvider):
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

    @property
    def model_name(self) -> str:
        return "fake-embedding"

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
