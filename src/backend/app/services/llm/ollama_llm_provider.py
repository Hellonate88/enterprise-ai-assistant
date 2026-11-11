from ollama import Client

from app.services.llm.llm_provider import LLMProvider


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
            ],
            options={"temperature": 0}
        )

        return response["message"]["content"]