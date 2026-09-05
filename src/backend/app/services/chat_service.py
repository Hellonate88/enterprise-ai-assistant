from app.services.retrieval_service import RetrievalService
from app.services.llm.llm_service import LLMService
from app.services.llm.prompt_service import PromptService



class ChatService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: LLMService
    ):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    def ask(
        self,
        question: str,
        top_k: int = 3
    ) -> dict:

        retrieved_docs = self.retrieval_service.retrieve(
            query=question,
            top_k=top_k
        )

        # Build context from retrieved documents
        context = "\n".join([doc["content"] for doc in retrieved_docs])

        # Construct RAG prompt with system instructions
        prompt = PromptService().build_rag_prompt(
            context=context,
            question=question
        )

        # Generate answer with error handling
        try:
            answer = self.llm_service.generate(prompt)
        except Exception as e:
            raise RuntimeError(
                "Failed to communicate with LLM provider. "
                "Please ensure the LLM service is running."
            ) from e

        # Extract sources (chunk IDs)
        sources = [f"chunk_{doc['chunk_id']}" for doc in retrieved_docs]

        return {
            "answer": answer,
            "sources": sources
        }