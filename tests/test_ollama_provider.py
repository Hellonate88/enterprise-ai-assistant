from app.services.llm.ollama_llm_provider import OllamaLLMProvider


def test_ollama_provider():

    provider = OllamaLLMProvider(
        model="llama3.2"
    )

    response = provider.generate(
        "Say hello in one sentence."
    )

    assert isinstance(response, str)

    assert len(response) > 0