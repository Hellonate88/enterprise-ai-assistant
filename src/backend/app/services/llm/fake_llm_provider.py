from app.services.llm.llm_provider import LLMProvider


class FakeLLMProvider(LLMProvider):

    def generate(
        self,
        prompt: str
    ) -> str:

        return (
            "This is a simulated AI response. "
            "No real LLM provider is currently configured."
        )