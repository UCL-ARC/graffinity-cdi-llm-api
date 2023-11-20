"""Define fixtures for model calling tests"""
import pytest

from llm_api.config import Settings


@pytest.fixture()
def mock_openai_client(mocker):
    return mocker.patch("llm_api.backends.openai.OpenaiCaller.client")


@pytest.fixture()
def mock_settings():
    return Settings(openai_api_key="test_fixture_key", llm_name="test-fixture-model")
