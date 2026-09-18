"""
API routes for the Study Assistant.

- GET  /health  -> simple liveness check
- POST /query   -> retrieve -> build prompt -> call Ollama -> grounded answer
"""

import logging

from fastapi import APIRouter, HTTPException

from app.schemas.query import QueryRequest, QueryResponse
from app.services.generation import generate_grounded_answer
from app.services.retrieval import retrieval_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """Lightweight endpoint used to confirm the API is up and reachable."""
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    """
    Answer a user's question using retrieval-augmented generation:
      1. Retrieve the most relevant chunks from the persisted vector store.
      2. Ask the local Ollama LLM to answer using ONLY that context.
      3. Return the answer plus the sources it was grounded on.
    """
    question = request.question.strip()
    if not question:
        # Pydantic's min_length=1 on QueryRequest already rejects empty
        # strings with a 422 before we even get here, but we keep this
        # defensive check in case that validation ever changes.
        raise HTTPException(status_code=422, detail="Question must not be empty.")

    try:
        chunks = retrieval_service.retrieve_relevant_chunks(question)
        answer_text, sources = generate_grounded_answer(question, chunks)
        return QueryResponse(answer=answer_text, sources=sources)

    except Exception as exc:  # noqa: BLE001 - we want a clean 500 for any failure
        logger.exception("Failed to answer question: %s", question)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the answer. Please try again.",
        ) from exc
