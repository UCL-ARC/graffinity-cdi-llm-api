"""Define fixtures for model calling tests"""
from collections.abc import Generator, AsyncGenerator
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from pydantic import SecretStr
from llm_api.config import BedrockModel, GPTModel, Settings
from fastapi.testclient import TestClient
from llm_api.main import app
from httpx import AsyncClient, ASGITransport


def get_app() -> FastAPI:
    """
    Return the FastAPI application instance for testing.

    Returns:
        FastAPI: The FastAPI application instance.

    """
    return app


@pytest.fixture()
def mock_openai_client(mocker):
    return mocker.patch("llm_api.backends.openai.OpenaiCaller.client")


@pytest.fixture()
def mock_settings():
    return Settings(
        openai_api_key=SecretStr("test_fixture_key"),
        openai_llm_name=GPTModel.GPT4,
        aws_access_key_id="dummy-access-id",
        aws_secret_access_key=SecretStr("dummy-secret-key"),
        aws_bedrock_model_id=BedrockModel.CLAUDE,
    )

@pytest.fixture(autouse=True)
def set_test_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[None, None, None]:
    """Configure the pytest environment."""
    monkeypatch.setenv("ENV", "local")
    monkeypatch.setenv("LLM_API_OPENAI_API_KEY", "a-fake-key")
    monkeypatch.setenv("LLM_API_OPENAI_LLM_NAME", "gpt-4-1106-preview")
    monkeypatch.setenv("LLM_API_AWS_ACCESS_KEY_ID", "a-fake-access-key-id")
    monkeypatch.setenv("LLM_API_AWS_SECRET_ACCESS_KEY", "a-fake-secret-access-key")
    monkeypatch.setenv("LLM_API_AWS_BEDROCK_MODEL_ID", "anthropic.claude-v2")
    yield
    monkeypatch.delenv("ENV")
    monkeypatch.delenv("LLM_API_OPENAI_API_KEY")
    monkeypatch.delenv("LLM_API_OPENAI_LLM_NAME")
    monkeypatch.delenv("LLM_API_AWS_ACCESS_KEY_ID")
    monkeypatch.delenv("LLM_API_AWS_SECRET_ACCESS_KEY")
    monkeypatch.delenv("LLM_API_AWS_BEDROCK_MODEL_ID")

@pytest.fixture
def test_sync_client(set_test_environment_variables) -> Generator[TestClient, None, None]:
    client = TestClient(get_app())
    yield client
    client.close()

@pytest.fixture
@asynccontextmanager
async def test_async_client(set_test_environment_variables) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=get_app()), base_url="http://test") as ac:
        yield ac
