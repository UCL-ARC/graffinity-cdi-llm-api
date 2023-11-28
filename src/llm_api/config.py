"""Define API settings."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Store typed settings for Pydantic."""

    openai_api_key: SecretStr
    llm_name: str
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
