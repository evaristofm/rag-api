import ollama

from app.core.config import settings


class LLMService:
    @staticmethod
    def ask(question: str, context: str) -> str:
        prompt = f"""Use the following context to answer the question.
If the context doesn't contain relevant information, say so.

Context:
{context}

Question: {question}"""

        response = ollama.chat(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
