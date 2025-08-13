"""API tests."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from llm_api.backends.bedrock import BedrockCaller, BedrockModelCallError
from llm_api.backends.openai import OpenaiCaller, OpenaiModelCallError
from llm_api.main import app

sync_client = TestClient(app)

def test_ping() -> None:
    """Test basic API functionality."""
    response = sync_client.get("/ping")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ping": "pong"}


@pytest.mark.asyncio
async def test_call_model_openai(mocker, test_async_client):

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
    async with test_async_client as ac:
        payload = {"user_search": "imagery and symbolism in macbeth"}
        response = await ac.post("/call_model_openai", json=payload)

        assert response.json()["entities"] == model_output["entities"]
        assert response.json()["connections"] == model_output["connections"]
        assert response.json()["user_search"] == payload["user_search"]


@pytest.mark.asyncio
async def test_call_model_openai_failure(mocker, test_async_client):

    mocker.patch.object(OpenaiCaller, "call_model", side_effect=OpenaiModelCallError)
    async with test_async_client as ac:
        payload = {"user_search": "imagery and symbolism in macbeth"}
        response = await ac.post("/call_model_openai", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_call_model_bedrock(mocker, test_async_client):

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
    async with test_async_client as ac:
        payload = {"user_search": "imagery and symbolism in macbeth"}
        response = await ac.post("/call_model_bedrock", json=payload)

        assert response.json()["entities"] == model_output["entities"]
        assert response.json()["connections"] == model_output["connections"]
        assert response.json()["user_search"] == payload["user_search"]


@pytest.mark.asyncio
async def test_call_model_bedrock_failure(mocker, test_async_client):

    mocker.patch.object(BedrockCaller, "call_model", side_effect=BedrockModelCallError)
    async with test_async_client as ac:
        payload = {"user_search": "imagery and symbolism in macbeth"}
        response = await ac.post("/call_model_bedrock", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
