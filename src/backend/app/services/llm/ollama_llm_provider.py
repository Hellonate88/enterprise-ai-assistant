from ollama import chat

from app.services.llm.llm_provider import LLMProvider
from app.core.config import settings


class OllamaLLMProvider(LLMProvider):

    def __init__(
        self,
        model: str
    ):
        self.model = model


    def generate(
        self,
        prompt: str
    ) -> str:

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content