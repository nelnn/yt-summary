import pytest
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.openai import OpenAI

from src.llm_config import llm_configs
from src.schemas.enums import LLMProvidersEnum
from src.schemas.models import LLMModel, YoutubeTranscriptRaw
from src.summarisers.base_summariser import BaseSummariser


class MockBaseSummariser(BaseSummariser):
    async def summarise(self, transcript: YoutubeTranscriptRaw) -> str:
        return "Mocked Summary"


@pytest.mark.parametrize(
    "provider,model_class,embed_class",
    [
        (LLMProvidersEnum.OPENAI, OpenAI, OpenAIEmbedding),
        (LLMProvidersEnum.GOOGLE, GoogleGenAI, GoogleGenAIEmbedding),
        (LLMProvidersEnum.ANTHROPIC, Anthropic, OpenAIEmbedding),
    ],
)
def test_get_model(provider, model_class, embed_class):
    llm = LLMModel(provider=provider, model=llm_configs[provider].default_model)
    summariser = MockBaseSummariser(llm)
    assert isinstance(summariser.model.llm, model_class)
    assert isinstance(summariser.model.embed_model, embed_class)


@pytest.mark.asyncio
async def test_summarise(llm_openai, fake_youtube_transcript_raw):
    summariser = MockBaseSummariser(llm_openai)
    summary = await summariser.summarise(fake_youtube_transcript_raw)
    assert summary == "Mocked Summary"
