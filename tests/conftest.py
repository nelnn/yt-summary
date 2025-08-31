from unittest.mock import AsyncMock

import pytest
from pydantic import HttpUrl
from youtube_transcript_api import FetchedTranscript, FetchedTranscriptSnippet

from yt_summary.llm_config import llm_configs
from yt_summary.schemas.enums import LLMProvidersEnum
from yt_summary.schemas.models import LLMModel, YoutubeMetadata, YoutubeTranscriptRaw


@pytest.fixture
def fake_fetched_transcript():
    return FetchedTranscript(
        snippets=[FetchedTranscriptSnippet(text="This is a mocked transcript.", start=0.0, duration=5.0)],
        video_id="dQw4w9WgXcQ",
        is_generated=False,
        language="en",
        language_code="en",
    )


@pytest.fixture
def fake_youtube_metadata():
    return YoutubeMetadata(
        video_id="dQw4w9WgXcQ",
        title="Test Video",
        author="Test Author",
        channel_id="channel123",
        video_url=HttpUrl("http://youtube.com/watch?v=123"),
        channel_url=HttpUrl("http://youtube.com/channel/channel123"),
        thumbnail_url=HttpUrl("http://youtube.com/thumbnail.jpg"),
        is_generated=False,
        language="en",
        language_code="en",
    )


@pytest.fixture
def fake_youtube_transcript_raw(fake_youtube_metadata):
    return YoutubeTranscriptRaw(
        metadata=fake_youtube_metadata,
        text="This is a test transcript.",
    )


@pytest.fixture
def fake_youtube_metadata_json():
    return {
        "title": "foo",
        "author_name": "bar",
        "author_url": "https://www.youtube.com/@baz",
        "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9W/hqdefault.jpg",
    }


@pytest.fixture
def mock_transcript(fake_youtube_metadata):
    mock = AsyncMock()
    mock.fetch.return_value = YoutubeTranscriptRaw(
        metadata=fake_youtube_metadata,
        text="This is a test transcript.",
    )
    return mock


@pytest.fixture
def mock_summariser():
    mock = AsyncMock()
    mock.summarise.return_value = "This is a summary."
    return mock


@pytest.fixture
def llm_openai():
    return LLMModel(
        provider=LLMProvidersEnum.OPENAI,
        model=llm_configs[LLMProvidersEnum.OPENAI].default_model,
    )
