"""API tests."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pydantic import SecretStr
from pydantic_settings import BaseSettings

from llm_api.backends.openai import OpenaiCaller
from llm_api.main import app
from llm_api.config import get_settings

sync_client = TestClient(app)

class TestSettings(BaseSettings):

    openai_api_key: SecretStr = SecretStr("test_inplace_key")
    llm_name: str = "test-inplace-model"

def get_test_settings():
    return TestSettings()

app.dependency_overrides[get_settings] = get_test_settings

def test_ping() -> None:
    """Test basic API functionality."""
    response = sync_client.get("/ping")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ping": "pong"}

@pytest.mark.asyncio
async def test_call_model(mocker):

    model_output = {
        "entities": [
            {
                "uri": "Imagery in Macbeth",
                "description": "The use of vivid or figurative language to represent objects, actions, or ideas.",
                "wikipedia_url": "https://en.wikipedia.org/wiki/Macbeth#Themes_and_motifs"
            },
        ],
        "connections": [
            {
                "from": "Imagery in Macbeth",
                "to": "Macbeth",
                "label": "is a theme in"
            },
        ]
    }

    mocker.patch.object(
        OpenaiCaller,
        "call_model",
        return_value = model_output.copy()
    )
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "user_search": "imagery and symbolism in macbeth"
        }
        response = await ac.post("/call_model", json=payload)

        assert response.json()["entities"] == model_output["entities"]
        assert response.json()["connections"] == model_output["connections"]
        assert response.json()["user_search"] == payload["user_search"]
