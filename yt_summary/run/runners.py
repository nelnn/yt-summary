"""Runner functions to simplify usage of the package."""

from yt_summary.extractors.transcript import TranscriptExtractor
from yt_summary.schemas.enums import LLMProvidersEnum, SummarisationModesEnum
from yt_summary.schemas.models import LLMModel
from yt_summary.summarisers.simple_summariser import SimpleSummariser
from yt_summary.summarisers.timestamp_summariser import RefinedSummariser


async def get_youtube_summary(
    url: str,
    llm_provider: LLMProvidersEnum = LLMProvidersEnum.OPENAI,
    model_name: str = "gpt-5-mini-2025-08-07",
    mode: SummarisationModesEnum = SummarisationModesEnum.SIMPLE,
) -> str:
    """Run the summarisation pipeline.

    Args:
        url (str): The YouTube video URL.
        llm_provider (str, optional): The LLM provider to use. Defaults to "openai".
        model_name (str, optional): The model name to use. Defaults to "gpt-5-mini-2025-08-07".
        mode (str, optional): The summarisation mode. Defaults to "simple".

    Returns:
        str: The summary of the YouTube video.

    """
    transcript = await TranscriptExtractor().fetch(url)
    match mode:
        case SummarisationModesEnum.SIMPLE:
            summariser = SimpleSummariser(llm=LLMModel(provider=LLMProvidersEnum(llm_provider), model=model_name))
        case SummarisationModesEnum.REFINE:
            summariser = RefinedSummariser(llm=LLMModel(provider=LLMProvidersEnum(llm_provider), model=model_name))
    return await summariser.summarise(transcript)
