"""
Tests for the /query endpoint using FastAPI's TestClient.

Run with:
    cd backend
    pytest -v

Note: the happy-path test monkeypatches the retrieval and generation
services so it does NOT require a real Ollama server or a populated
vector store to run -- this keeps CI/unit tests fast and independent of
external services, while still exercising the real endpoint logic.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.query import SourceChunk
from app.services.retrieval import RetrievedChunk

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.api.routes.query.generate_grounded_answer")
@patch("app.api.routes.query.retrieval_service")
def test_query_happy_path(mock_retrieval_service, mock_generate_grounded_answer):
    # Arrange: fake a retrieved chunk and a fake LLM answer, so this test
    # does not depend on Ollama or the real vector store being available.
    mock_retrieval_service.retrieve_relevant_chunks.return_value = [
        RetrievedChunk(
            chunk_id="chunk_1",
            text="A variable is a named container used to store a value.",
            source="python_basics.pdf",
            distance=0.12,
        )
    ]
    mock_generate_grounded_answer.return_value = (
        "A variable is a named container used to store a value in memory. [1]",
        [
            SourceChunk(
                source="python_basics.pdf",
                chunk_id="chunk_1",
                snippet="A variable is a named container used to store a value.",
            )
        ],
    )

    # Act
    response = client.post("/query", json={"question": "What is a variable?"})

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    assert "sources" in body
    assert len(body["sources"]) == 1
    assert body["sources"][0]["source"] == "python_basics.pdf"


def test_query_invalid_input_returns_422():
    # Missing the required "question" field entirely.
    response = client.post("/query", json={})
    assert response.status_code == 422

    # Empty question string also violates min_length=1.
    response = client.post("/query", json={"question": ""})
    assert response.status_code == 422
