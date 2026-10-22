from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "AI Knowledge Assistant"

    llm_provider: str = "ollama"

    ollama_model: str = "llama3.2"

    ollama_base_url: str = "http://localhost:11434"

    embedding_provider: str = "ollama"

    ollama_embedding_model: str = "nomic-embed-text"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()