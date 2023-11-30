"""Define API settings."""
from enum import StrEnum

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class GPTModel(StrEnum):
    """Define possible GPT models."""

    GPT4 = "gpt-4-1106-preview"
    GPT3 = "gpt-3.5-turbo-1106"


class BedrockModel(StrEnum):
    """Define possible Bedrock models."""

    CLAUDE = "anthropic.claude-v2"
    CLAUDE_INSTANT = "anthropic.claude-instant-v1"


class Settings(BaseSettings):
    """Store typed settings for Pydantic."""

    openai_api_key: SecretStr
    openai_llm_name: GPTModel
    aws_access_key_id: str
    aws_secret_access_key: SecretStr
    aws_bedrock_model_id: BedrockModel
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="LLM_API_"
    )


def get_settings() -> Settings:
    """
    Return a Settings object.

    Returns
        Settings: Pydantic settings object
    """
    return Settings()
