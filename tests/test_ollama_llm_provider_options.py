from unittest.mock import patch

from src.backend.app.services.llm.ollama_llm_provider import (
    OllamaLLMProvider,
)


def test_generate_uses_deterministic_temperature():
    with patch(
        "src.backend.app.services.llm.ollama_llm_provider.Client"
    ) as client_class:
        client = client_class.return_value
        client.chat.return_value = {"message": {"content": "15 days."}}
        provider = OllamaLLMProvider(
            model="llama3.2",
            base_url="http://localhost:11434",
        )

        answer = provider.generate("How many sick leave days?")

    assert answer == "15 days."
    client.chat.assert_called_once_with(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": "How many sick leave days?",
            }
        ],
        options={"temperature": 0},
    )
