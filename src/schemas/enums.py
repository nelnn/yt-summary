"""Enums."""

from enum import StrEnum


class LLMProvidersEnum(StrEnum):
    """Enum for different Large Language Models (LLMs)."""

    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"


class SummarisationModeEnum(StrEnum):
    """Enum for different summarization modes."""

    SIMPLE = "simple"
    REFINE = "refine"


class FileFormatEnum(StrEnum):
    """Enum for different file formats."""

    TXT = "txt"
    MD = "md"
    HTML = "html"
