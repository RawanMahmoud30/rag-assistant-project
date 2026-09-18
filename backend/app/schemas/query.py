"""
Pydantic schemas: these define the exact "shape" of the JSON that the
/query endpoint accepts and returns. FastAPI uses them to validate incoming
requests automatically (that's how we get a free HTTP 422 on bad input).
"""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="The user's natural-language question about the documents.",
        examples=["What is a variable in Python?"],
    )


class SourceChunk(BaseModel):
    """One retrieved chunk that was used to ground the answer."""
    source: str = Field(..., description="Original document/file name.")
    chunk_id: str = Field(..., description="Identifier of the chunk within the vector store.")
    snippet: str = Field(..., description="Short preview of the chunk text used for the answer.")


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
