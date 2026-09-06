from app.core.config import settings

from app.services.llm.llm_provider import LLMProvider
from app.services.llm.fake_llm_provider import FakeLLMProvider
from app.services.llm.ollama_llm_provider import OllamaLLMProvider


class LLMProviderFactory:

    @staticmethod
    def create() -> LLMProvider:

        if settings.llm_provider == "fake":

            return FakeLLMProvider()


        if settings.llm_provider == "ollama":

            return OllamaLLMProvider(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url
            )


        raise ValueError(
            f"Unsupported LLM provider: "
            f"{settings.llm_provider}"
        )