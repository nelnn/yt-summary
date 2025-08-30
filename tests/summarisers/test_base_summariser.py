import pytest
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.openai import OpenAI
from pydantic import HttpUrl

from src.llm_config import llm_configs
from src.schemas.enums import LLMEnum
from src.schemas.models import LLMModel, YoutubeMetadata, YoutubeTranscriptRaw
from src.summarisers.base_summariser import BaseSummariser


class MockBaseSummariser(BaseSummariser):
    async def summarise(self, transcript: YoutubeTranscriptRaw) -> str:
        return "Mocked Summary"


@pytest.fixture
def llm_openai():
    return LLMModel(
        provider=LLMEnum.OPENAI,
        model=llm_configs[LLMEnum.OPENAI].default_model,
    )


@pytest.fixture
def llm_google():
    return LLMModel(
        provider=LLMEnum.GOOGLE,
        model=llm_configs[LLMEnum.GOOGLE].default_model,
    )


@pytest.fixture
def llm_anthropic():
    return LLMModel(
        provider=LLMEnum.ANTHROPIC,
        model=llm_configs[LLMEnum.ANTHROPIC].default_model,
    )


class TestBaseSummariser:
    def test_init_openai(self, llm_openai):
        summariser = MockBaseSummariser(llm_openai)
        assert isinstance(summariser.model.llm, OpenAI)
        assert isinstance(summariser.model.embed_model, OpenAIEmbedding)

    def test_init_google(self, llm_google):
        summariser = MockBaseSummariser(llm_google)
        assert isinstance(summariser.model.llm, GoogleGenAI)
        assert isinstance(summariser.model.embed_model, GoogleGenAIEmbedding)

    def test_init_anthropic(self, llm_anthropic):
        summariser = MockBaseSummariser(llm_anthropic)
        assert isinstance(summariser.model.llm, Anthropic)
        assert isinstance(summariser.model.embed_model, OpenAIEmbedding)

    @pytest.mark.asyncio
    async def test_summarise(self, llm_openai):
        summariser = MockBaseSummariser(llm_openai)
        transcript = YoutubeTranscriptRaw(
            text="This is a mocked transcript.",
            metadata=YoutubeMetadata(
                video_id="dQw4w9WgXcQ",
                title="foo",
                author="bar",
                channel_id="@baz",
                video_url=HttpUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                channel_url=HttpUrl("https://www.youtube.com/channel/@baz"),
                thumbnail_url=HttpUrl("https://i.ytimg.com/vi/dQw4w9W/hqdefault.jpg"),
            ),
        )
        summary = await summariser.summarise(transcript)
        assert summary == "Mocked Summary"
