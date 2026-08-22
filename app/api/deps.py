from functools import lru_cache

from app.services.llm import LLMService
from app.services.vector_store import VectorStoreService


@lru_cache
def get_vector_store_service() -> VectorStoreService:
    return VectorStoreService()


@lru_cache
def get_llm_service() -> LLMService:
    return LLMService()
