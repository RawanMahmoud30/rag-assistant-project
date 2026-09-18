import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://localhost:8000"
)


class BackendError(Exception):
    """Raised when the backend is unreachable or returns an error."""


def check_health(timeout: float = 3.0) -> bool:
    try:
        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=timeout
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def ask_question(question: str, timeout: float = 180.0) -> dict:
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question},
            timeout=timeout
        )

    except requests.ConnectionError as exc:
        raise BackendError(
            f"Could not reach the backend at {API_BASE_URL}. "
            "Is it running?"
        ) from exc

    except requests.Timeout as exc:
        raise BackendError(
            "The backend took too long to respond. Please try again."
        ) from exc

    if response.status_code == 422:
        raise BackendError(
            "Please enter a valid, non-empty question."
        )

    if response.status_code >= 500:
        raise BackendError(
            "The backend ran into an error while generating the answer."
        )

    if not response.ok:
        raise BackendError(
            f"Unexpected error from backend "
            f"(status {response.status_code})."
        )

    return response.json()