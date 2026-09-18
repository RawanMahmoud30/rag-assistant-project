"""
Application configuration.

All settings are read from environment variables (or a `.env` file in the
`backend/` folder). This means we never hard-code things like model names,
paths, or the frontend's URL directly in the code -- we can change them
without touching a single line of Python.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Vector store -------------------------------------------------
    # Path to the Chroma persistent directory produced by the notebook
    # (notebooks/rag_pipeline.ipynb, section 3.12 "Export/Persist Vector Store").
    VECTOR_STORE_DIR: str = "./data/vector_store"
    CHROMA_COLLECTION_NAME: str = "study_assistant_docs"

    # --- Embeddings -----------------------------------------------------
    # Must be the SAME embedding model used to build the vector store in the
    # notebook, otherwise similarity search will be meaningless.
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # --- Ollama LLM -------------------------------------------------------
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # --- Retrieval --------------------------------------------------------
    TOP_K: int = 4

    # --- CORS ---------------------------------------------------------
    # Comma-separated list of allowed origins for the frontend.
    FRONTEND_ORIGINS: str = "http://localhost:8501"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def frontend_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.FRONTEND_ORIGINS.split(",") if origin.strip()]


# A single, shared settings object imported everywhere else in the app.
settings = Settings()
