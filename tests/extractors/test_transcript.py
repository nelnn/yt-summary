from unittest import mock

import pytest
from pydantic import HttpUrl

from yt_summary.extractors.transcript import TranscriptExtractor
from yt_summary.schemas.models import YoutubeMetadata, YoutubeTranscriptRaw


@pytest.fixture
def url():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@pytest.fixture(autouse=True)
def patch_fetch_transcript(monkeypatch):
    def mock_fetch_transcript(url, languages=None, *, preserve_formatting=False):
        return "This is a mocked transcript."

    monkeypatch.setattr("yt_summary.extractors.transcript.TranscriptExtractor.fetch_transcript", mock_fetch_transcript)


class TestTranscriptExtractor:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.extractor = TranscriptExtractor()

    def test_fetch_transcript(self, url):
        transcript = self.extractor.fetch_transcript(url)
        assert transcript == "This is a mocked transcript."

    @pytest.mark.asyncio
    async def test__afetch_transcript(self, url):
        with mock.patch.object(
            self.extractor, "fetch_transcript", return_value="This is a mocked transcript."
        ) as mock_fetch:
            transcript = await self.extractor._afetch_transcript(url)
            mock_fetch.assert_called_once_with(url=url, languages=None, preserve_formatting=False)
            assert transcript == "This is a mocked transcript."

    @pytest.mark.asyncio
    async def test_fetch(self, url):
        mock_metadata = YoutubeMetadata(
            video_id="dQw4w9WgXcQ",
            title="foo",
            author="bar",
            channel_id="@baz",
            video_url=HttpUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
            channel_url=HttpUrl("https://www.youtube.com/channel/@baz"),
            thumbnail_url=HttpUrl("https://i.ytimg.com/vi/dQw4w9W/hqdefault.jpg"),
        )

        with (
            mock.patch("yt_summary.extractors.transcript.extract_metadata", return_value=mock_metadata),
            mock.patch.object(self.extractor, "_afetch_transcript", return_value="This is a mocked transcript."),
        ):
            result = await self.extractor.fetch(url, languages=["en", "de"])

            expected_result = YoutubeTranscriptRaw(text="This is a mocked transcript.", metadata=mock_metadata)
            assert result == expected_result
