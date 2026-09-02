from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier for this provider."""
        pass

    @abstractmethod
    def generate_embedding(self, text: str) -> list[float]:
        pass