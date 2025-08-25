"""Enviroment configuration for the application."""

import asyncpg
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.database.context_manager import DBSession, db_engine


class Settings(BaseSettings):
    """Settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # FASTAPI
    API_TITLE: str = "Youtube Rag"
    API_DESCRIPTION: str = "A simple Youtube RAG application"
    API_VERSION: str = "1.0.0"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost"]
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # POSTGRESQL
    POSTGRES_USER: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    POSTGRES_CONNECTION_STR: str = ""

    # OPENAI
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""

    MIGRATIONS_FOLDER_PATH: str = "migrations"

    @field_validator("POSTGRES_CONNECTION_STR", mode="before")
    def assemble_wms_sqlalchemy_connection_string(cls, v: str, info: ValidationInfo) -> str:
        """Assemble the PostgreSQL connection string from environment variables."""
        return f"postgresql://{info.data['POSTGRES_USER']}:{info.data['POSTGRES_PASSWORD']}@{info.data['POSTGRES_HOST']}:{info.data['POSTGRES_PORT']}/{info.data['POSTGRES_DB']}"


settings = Settings()
db_conn = DBSession(settings.POSTGRES_CONNECTION_STR)
engine = db_engine(settings.POSTGRES_CONNECTION_STR)
