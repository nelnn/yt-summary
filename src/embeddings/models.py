"""Embedding models"""

from enum import StrEnum


class EmbeddingModel(StrEnum):
    """Enum for embedding models."""

    OPENAI = "openai"
    GOOGLE = "google"


embedding_models = {
    "openai": EmbeddingModel.OPENAI,
}
