from enum import StrEnum


class LLMEnum(StrEnum):
    """Enum for different Large Language Models (LLMs)."""

    OPENAI = "openai"
    GOOGLE = "google"


class SummarisationModeEnum(StrEnum):
    """Enum for different summarization modes."""

    SIMPLE = "simple"
    DETAILED = "detailed"
