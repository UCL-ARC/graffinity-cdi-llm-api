"""API tests."""
from fastapi import status
from fastapi.testclient import TestClient

from llm_api.main import app

client = TestClient(app)


def test_ping() -> None:
    """Test basic API functionality."""
    response = client.get("/ping")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ping": "pong"}
