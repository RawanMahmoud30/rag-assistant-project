"""
Retrieval service.

Responsible for:
  1. Loading the ALREADY-BUILT Chroma vector store from disk (built once by
     the notebook, at notebooks/rag_pipeline.ipynb). We never rebuild
     embeddings here -- that would be slow and would defeat the point of
     persisting the vector store.
  2. Embedding the user's question with the SAME embedding model used to
     build the store.
  3. Returning the top-k most similar chunks, with their source metadata.

This module exposes a single reusable function, `retrieve_relevant_chunks`,
which is intentionally written the same way it is used in the notebook so
that behaviour stays identical between "notebook experiments" and "backend
in production".
"""

from dataclasses import dataclass

import chromadb
from chromadb.utils import embedding_functions

from app.core.config import settings


@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    source: str
    distance: float


class RetrievalService:
    """Wraps a persistent Chroma collection + embedding function."""

    def __init__(self) -> None:
        # PersistentClient just points at a folder on disk; it does NOT
        # recompute anything that is already there.
        self._client = chromadb.PersistentClient(path=settings.VECTOR_STORE_DIR)

        # Must match the embedding model used in the notebook when the
        # collection was created, or similarity search will be meaningless.
        self._embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL_NAME
        )

        self._collection = self._client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=self._embedding_fn,
        )

    def collection_is_populated(self) -> bool:
        return self._collection.count() > 0

    def retrieve_relevant_chunks(self, question: str, top_k: int | None = None) -> list[RetrievedChunk]:
        """
        Given a raw user question, return the top_k most similar chunks
        (text + source file + a similarity distance) from the vector store.
        """
        k = top_k or settings.TOP_K

        results = self._collection.query(
            query_texts=[question],
            n_results=k,
        )

        chunks: list[RetrievedChunk] = []
        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for chunk_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
            chunks.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    text=text,
                    source=(metadata or {}).get("source", "unknown"),
                    distance=distance,
                )
            )
        return chunks


# A single shared instance, created once and reused by every request
# (loaded at FastAPI startup -- see app/main.py).
retrieval_service = RetrievalService()
