import os


class Settings:
    def __init__(self):
        self.chroma_db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        self.chroma_collection_name = os.getenv(
            "CHROMA_COLLECTION_NAME", "personal_profile"
        )
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.llm_model = os.getenv("LLM_MODEL", "qwen2.5:0.5b")


settings = Settings()
