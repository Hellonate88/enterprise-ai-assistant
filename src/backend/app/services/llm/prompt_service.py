class PromptService:

    def build_rag_prompt(
        self,
        context: str,
        question: str
    ) -> str:
        return f"""You are a helpful assistant.

            Answer the question using ONLY the provided context.

            If the answer cannot be found in the context,
            say that you do not know.

            Context:

            {context}

            Question:

            {question}
            """