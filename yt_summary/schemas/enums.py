"""Enums."""

from enum import StrEnum


class LLMProvidersEnum(StrEnum):
    """Enum for different Large Language Models (LLMs)."""

    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"


class SummarisationModesEnum(StrEnum):
    """Enum for different summarization modes."""

    SIMPLE = "simple"
    REFINE = "refine"
