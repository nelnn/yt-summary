"""Enviroment configuration for the application."""

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from yt_summary.schemas.enums import LLMProvidersEnum


class Settings(BaseSettings):
    """Settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # FASTAPI (future use)
    API_TITLE: str = "Youtube Rag"
    API_DESCRIPTION: str = "A simple Youtube RAG application"
    API_VERSION: str = "1.0.0"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost"]
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # LLM API
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5-mini-2025-08-07"
    GOOGLE_API_KEY: str = ""
    GOOGLE_MODEL: str = "gemini-1.5-flash"
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-haiku-20241022"

    MIGRATIONS_FOLDER_PATH: str = "migrations"


settings = Settings()


class LLMConfigs(BaseModel):
    """Language model configurations.

    Attributes:
        key_env: Environment variable name for the API key.
        default_key: Default API key if environment variable is not set.
        default_model: Default model name to use.

    """

    key_name: str
    default_key: str
    default_model: str


class OPENAIConfig(LLMConfigs):
    """OpenAI model configuration."""

    key_name: str = "OPENAI_API_KEY"
    default_key: str = settings.OPENAI_API_KEY
    default_model: str = settings.OPENAI_MODEL


class GOOGLEConfig(LLMConfigs):
    """Google model configuration."""

    key_name: str = "GOOGLE_API_KEY"
    default_key: str = settings.GOOGLE_API_KEY
    default_model: str = settings.GOOGLE_MODEL


class ANTHROPICConfig(LLMConfigs):
    """Anthropic model configuration."""

    key_name: str = "ANTHROPIC_API_KEY"
    default_key: str = settings.ANTHROPIC_API_KEY
    default_model: str = settings.ANTHROPIC_MODEL


llm_configs: dict[LLMProvidersEnum, LLMConfigs] = {
    LLMProvidersEnum.OPENAI: OPENAIConfig(),
    LLMProvidersEnum.GOOGLE: GOOGLEConfig(),
    LLMProvidersEnum.ANTHROPIC: ANTHROPICConfig(),
}
