from app.core.config import settings


def test_settings():

    print(settings.app_name)

    print(settings.llm_provider)

    print(settings.ollama_model)

    assert settings.llm_provider == "ollama"
    assert settings.ollama_model == "llama3.2"
    assert settings.ollama_base_url == "http://localhost:11434"