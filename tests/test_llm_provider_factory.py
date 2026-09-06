from app.services.llm.llm_provider_factory import (
    LLMProviderFactory
)

from app.services.llm.ollama_llm_provider import (
    OllamaLLMProvider
)


def test_factory_creates_ollama_provider():

    provider = LLMProviderFactory.create()

    assert isinstance(
        provider,
        OllamaLLMProvider
    )