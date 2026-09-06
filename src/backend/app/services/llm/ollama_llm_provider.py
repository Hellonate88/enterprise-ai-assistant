from ollama import Client, chat

from app.services.llm.llm_provider import LLMProvider
from app.core.config import settings


class OllamaLLMProvider(LLMProvider):

    def __init__(
        self,
        model: str,
        base_url: str
    ):
        self.model = model

        self.client = Client(
            host=base_url
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content