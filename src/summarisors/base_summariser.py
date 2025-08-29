"""Base class for text summarisation models."""

import abc
import os

from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.openai import OpenAI

from src.llm_config import llm_configs
from src.schemas.enums import LLMEnum
from src.schemas.models import LLMModel, YoutubeTranscriptRaw


class BaseSummariser(abc.ABC):
    """Base class for text summarisation models.

    Attributes:
        model: LLM model to use for summarisation.

    """

    def __init__(self, llm: LLMModel) -> None:
        self.model = self._get_model(llm)

    @staticmethod
    def _get_model(llm: LLMModel) -> FunctionCallingLLM:
        """Get the LLM model based on the provided configuration.

        Args:
            llm: LLM model model.

        Returns:
            An instance of the selected LLM model.

        """
        opts = llm_configs[llm.provider]
        os.environ[opts.key_name] = os.getenv(opts.key_name) or opts.default_key
        match llm.provider:
            case LLMEnum.OPENAI:
                llm_model = OpenAI(temperature=0, model=llm.model)
            case LLMEnum.GOOGLE:
                llm_model = GoogleGenAI(temperature=0, model=llm.model)
            case LLMEnum.ANTHROPIC:
                llm_model = Anthropic(temperature=0, model=llm.model)
        return llm_model

    @abc.abstractmethod
    async def summarise(self, transcript: YoutubeTranscriptRaw) -> str:
        """Abstract method to summarise text.

        Args:
            transcript: The transcript text to summarise.

        Returns:
            Summarised text.

        """
