"""API tests."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pydantic import SecretStr
from pydantic_settings import BaseSettings

from llm_api.backends.bedrock import BedrockCaller, BedrockModelCallError
from llm_api.backends.openai import OpenaiCaller, OpenaiModelCallError
from llm_api.config import BedrockModel, GPTModel, get_settings
from llm_api.main import app

sync_client = TestClient(app)


class TestSettings(BaseSettings):

    openai_api_key: SecretStr = SecretStr("test_fixture_key")
    openai_llm_name: GPTModel = GPTModel.GPT4
    aws_access_key_id: str = "dummy-access-id"
    aws_secret_access_key: SecretStr = SecretStr("dummy-secret-key")
    aws_bedrock_model_id: BedrockModel = BedrockModel.CLAUDE


def get_test_settings():
    return TestSettings()


app.dependency_overrides[get_settings] = get_test_settings


def test_ping() -> None:
    """Test basic API functionality."""
    response = sync_client.get("/ping")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ping": "pong"}


@pytest.mark.asyncio
async def test_call_model_openai(mocker):

    model_output = {
        "entities": [
            {
                "uri": "Imagery in Macbeth",
                "description": "The use of vivid or figurative language to represent objects, actions, or ideas.",
                "wikipedia_url": "https://en.wikipedia.org/wiki/Macbeth#Themes_and_motifs",
            },
        ],
        "connections": [
            {"from": "Imagery in Macbeth", "to": "Macbeth", "label": "is a theme in"},
        ],
    }

    mocker.patch.object(OpenaiCaller, "call_model", return_value=model_output.copy())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"user_search": "imagery and symbolism in macbeth"}
        response = await ac.post("/call_model_openai", json=payload)

        assert response.json()["entities"] == model_output["entities"]
        assert response.json()["connections"] == model_output["connections"]
        assert response.json()["user_search"] == payload["user_search"]


@pytest.mark.asyncio
async def test_call_model_openai_failure(mocker):

    mocker.patch.object(OpenaiCaller, "call_model", side_effect=OpenaiModelCallError)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"user_search": "imagery and symbolism in macbeth"}
        response = await ac.post("/call_model_openai", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_call_model_bedrock(mocker):

    model_output = {
        "entities": [
            {
                "uri": "Imagery in Macbeth",
                "description": "The use of vivid or figurative language to represent objects, actions, or ideas.",
                "wikipedia_url": "https://en.wikipedia.org/wiki/Macbeth#Themes_and_motifs",
            },
        ],
        "connections": [
            {"from": "Imagery in Macbeth", "to": "Macbeth", "label": "is a theme in"},
        ],
    }
    mocker.patch.object(BedrockCaller, "call_model", return_value=model_output.copy())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"user_search": "imagery and symbolism in macbeth"}
        response = await ac.post("/call_model_bedrock", json=payload)

        assert response.json()["entities"] == model_output["entities"]
        assert response.json()["connections"] == model_output["connections"]
        assert response.json()["user_search"] == payload["user_search"]


@pytest.mark.asyncio
async def test_call_model_bedrock_failure(mocker):

    mocker.patch.object(BedrockCaller, "call_model", side_effect=BedrockModelCallError)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"user_search": "imagery and symbolism in macbeth"}
        response = await ac.post("/call_model_bedrock", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
