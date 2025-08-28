"""Base class for text summarisation models."""

import abc
import os

import openai
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.openai import OpenAI

from src.config import llm_config
from src.schemas.enums import LLMEnum
from src.schemas.models import YoutubeTranscriptRaw


class BaseSummariser(abc.ABC):
    """Base class for text summarisation models.

    Attributes:
        model: LLM model to use for summarisation.

    """

    def __init__(self, model: LLMEnum) -> None:
        self.model = self._get_model(model)

    @staticmethod
    def _get_model(model: LLMEnum) -> FunctionCallingLLM:
        creds = llm_config[model]
        match model:
            case LLMEnum.OPENAI:
                os.environ["OPENAI_API_KEY"] = creds["key"]
                openai.api_key = os.environ["OPENAI_API_KEY"]
                llm = OpenAI(temperature=0, api_key=creds["key"], model=creds["model"])
            case LLMEnum.GOOGLE:
                llm = GoogleGenAI(temperature=0, api_key=creds["key"], model=creds["model"])
        return llm

    @abc.abstractmethod
    async def summarise(self, transcript: YoutubeTranscriptRaw) -> str:
        """Abstract method to summarise text.

        Args:
            transcript: The transcript text to summarise.

        Returns:
            Summarised text.

        """
