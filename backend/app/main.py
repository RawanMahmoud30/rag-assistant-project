"""
FastAPI application entrypoint.

Responsibilities:
  - Create the FastAPI app.
  - Configure CORS so the Streamlit frontend can call this API.
  - Load the vector store and Ollama connection ONCE at startup (via the
    `lifespan` context manager), not on every request.
  - Register the /health and /query routes.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.query import router as query_router
from app.core.config import settings
from app.utils.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Importing app.services.retrieval triggers RetrievalService.__init__,
    # which loads the persisted Chroma collection from disk exactly once.
    from app.services.retrieval import retrieval_service

    if retrieval_service.collection_is_populated():
        logger.info("Vector store loaded successfully and is populated.")
    else:
        logger.warning(
            "Vector store loaded but appears EMPTY. Did you run the "
            "notebook (rag_pipeline.ipynb) and export it to %s?",
            settings.VECTOR_STORE_DIR,
        )

    logger.info("Ollama target model: %s (host: %s)", settings.OLLAMA_MODEL, settings.OLLAMA_HOST)
    yield
    logger.info("Shutting down Study Assistant API.")


app = FastAPI(
    title="Study Assistant RAG API",
    description="Retrieval-Augmented Generation backend for the Study Assistant project.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)
