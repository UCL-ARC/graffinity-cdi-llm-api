"""Define fixtures for model calling tests"""
import pytest

from llm_api.config import Settings, GPTModel, BedrockModel


@pytest.fixture()
def mock_openai_client(mocker):
    return mocker.patch("llm_api.backends.openai.OpenaiCaller.client")


@pytest.fixture()
def mock_settings():
    return Settings(
        openai_api_key="test_fixture_key",
        openai_llm_name=GPTModel.GPT4,
        aws_access_key_id="dummy-access-id",
        aws_secret_access_key="dummy-secret-key",
        aws_bedrock_model_id=BedrockModel.CLAUDE
    )
