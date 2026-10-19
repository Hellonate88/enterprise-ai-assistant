class PromptService:

    def build_rag_prompt(
        self,
        context: str,
        question: str
    ) -> str:
        return f"""You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:

"I don't know based on the provided documents."

Do not use outside knowledge.

Context:
{context}

Question:
{question}"""