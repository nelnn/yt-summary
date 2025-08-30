import pytest
from pydantic import HttpUrl

from src.llm_config import llm_configs
from src.schemas.enums import LLMEnum
from src.schemas.models import LLMModel, YoutubeMetadata, YoutubeTranscriptRaw
from src.summarisers.simple_summariser import SimpleSummariser


@pytest.fixture
def llm_openai():
    return LLMModel(
        provider=LLMEnum.OPENAI,
        model=llm_configs[LLMEnum.OPENAI].default_model,
    )


@pytest.fixture(autouse=True)
def patch_summarise(monkeypatch):
    async def mock_summarise(self, transcript):
        return "Mocked Summary"

    monkeypatch.setattr("src.summarisers.simple_summariser.SimpleSummariser.summarise", mock_summarise)


class TestSimpleSummariser:
    @pytest.fixture(autouse=True)
    def setup(self, llm_openai):
        self.summariser = SimpleSummariser(llm_openai)

    @pytest.mark.asyncio
    async def test_summarise(self):
        transcript = YoutubeTranscriptRaw(
            text="This is a test transcript. It contains multiple sentences. The purpose is to test the summariser.",
            metadata=YoutubeMetadata(
                video_id="test_video",
                title="Test Video",
                author="Test Author",
                video_url=HttpUrl("http://example.com"),
                channel_url=HttpUrl("http://example.com/channel"),
                channel_id="",
                thumbnail_url=HttpUrl("http://example.com/thumb.jpg"),
            ),
        )
        summary = await self.summariser.summarise(transcript)
        assert summary == "Mocked Summary"
