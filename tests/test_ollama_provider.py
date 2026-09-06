from app.services.llm.ollama_llm_provider import OllamaLLMProvider


def test_ollama_provider():

    provider = OllamaLLMProvider(
        model="llama3.2",
        base_url="http://localhost:11434"
    )

    response = provider.generate(
        "Explain RAG in one short sentence."
    )

    print(response)

    assert isinstance(response, str)

    assert len(response) > 0