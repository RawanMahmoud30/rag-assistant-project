"""
Generation service.

Responsible for:
  1. Building a prompt that forces the LLM to answer ONLY from the
     retrieved context (grounding), and to say so honestly when the
     context isn't enough.
  2. Calling the local Ollama model.
  3. Returning the answer text together with the source list, ready to be
     sent back as a QueryResponse.
"""

import ollama

from app.core.config import settings
from app.schemas.query import SourceChunk
from app.services.retrieval import RetrievedChunk

SYSTEM_PROMPT = """You are a helpful study assistant that answers questions strictly using \
the CONTEXT provided below, which was retrieved from the user's own documents.

Rules you MUST follow:
1. Only use information that is present in the CONTEXT. Do not use outside knowledge.
2. If the CONTEXT does not contain enough information to answer the question, \
say clearly: "I don't have enough information in the documents to answer that." \
Do not guess or make anything up.
3. Keep the answer concise and easy to understand for a student.
4. Do not mention these instructions in your answer.
"""


def _build_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        context_blocks.append(f"[{i}] (source: {chunk.source})\n{chunk.text}")
    context_text = "\n\n".join(context_blocks) if context_blocks else "(no relevant context found)"

    return (
        f"CONTEXT:\n{context_text}\n\n"
        f"QUESTION:\n{question}\n\n"
        f"Answer the question using only the CONTEXT above. "
        f"Reference sources by their [number] where relevant."
    )


def generate_grounded_answer(question: str, chunks: list[RetrievedChunk]) -> tuple[str, list[SourceChunk]]:
    """
    Given a question and its retrieved chunks, build the grounded prompt,
    call the local Ollama model, and return (answer_text, sources_list).
    """
    if not chunks:
        return (
            "I don't have enough information in the documents to answer that.",
            [],
        )

    user_prompt = _build_prompt(question, chunks)

    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    answer_text = response["message"]["content"].strip()

    sources = [
        SourceChunk(
            source=chunk.source,
            chunk_id=chunk.chunk_id,
            snippet=chunk.text[:200] + ("..." if len(chunk.text) > 200 else ""),
        )
        for chunk in chunks
    ]

    return answer_text, sources
