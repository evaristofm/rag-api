import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

from app.core.config import settings


class VectorStoreService:
    def __init__(self):
        client = chromadb.PersistentClient(path=settings.chroma_db_path)
        embedding_function = OllamaEmbeddingFunction(
            model_name=settings.embedding_model,
            url=settings.ollama_url,
        )
        self.collection = client.get_or_create_collection(
            name=settings.chroma_collection_name,
            embedding_function=embedding_function,
        )

    def add_documents(self, ids: list[str], documents: list[str], metadatas: list[dict]):
        self.collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def query(
        self, question: str, n_results: int = 2, user_name: str | None = None
    ) -> list[str]:
        query_params = {"query_texts": [question], "n_results": n_results}

        if user_name:
            query_params["where"] = {"user_name": user_name}

        results = self.collection.query(**query_params)
        return results["documents"][0]
