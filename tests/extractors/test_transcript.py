from unittest import mock

import pytest
from youtube_transcript_api import FetchedTranscriptSnippet
from yt_summary.extractors.transcript import TranscriptExtractor


@pytest.fixture
def url():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@pytest.fixture
def snippets():
    return [
        FetchedTranscriptSnippet(text="This is", start=0.0, duration=5.0),
        FetchedTranscriptSnippet(text="a test. Snippet", start=5.0, duration=5),
        FetchedTranscriptSnippet(text="three!", start=10.0, duration=5.0),
    ]




@pytest.fixture(autouse=True)
def patch_fetch_transcript(monkeypatch, fake_fetched_transcript):
    def mock_fetch_transcript(url, languages=None, *, preserve_formatting=False):
        return fake_fetched_transcript
    monkeypatch.setattr("yt_summary.extractors.transcript.TranscriptExtractor.fetch_transcript", mock_fetch_transcript)


class TestTranscriptExtractor:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.extractor = TranscriptExtractor()

    def test_fetch_transcript(self, url, fake_fetched_transcript):
        transcript = self.extractor.fetch_transcript(url)
        assert transcript == fake_fetched_transcript

    @pytest.mark.asyncio
    async def test__afetch_transcript(self, url, fake_fetched_transcript):
        with mock.patch.object(
            self.extractor, "fetch_transcript", return_value=fake_fetched_transcript,
        ) as mock_fetch:
            transcript = await self.extractor._afetch_transcript(url)
            mock_fetch.assert_called_once_with(url=url, languages=None, preserve_formatting=False)
            assert transcript == fake_fetched_transcript

    @pytest.mark.asyncio
    async def test_fetch(self, url, fake_youtube_transcript_raw):
        with mock.patch.object(self.extractor, "fetch", return_value=fake_youtube_transcript_raw):
            result = await self.extractor.fetch(url, languages=["en", "de"])
            assert result == fake_youtube_transcript_raw



def test__stitch_snippets(snippets):
    extractor = TranscriptExtractor()
    text = extractor._stitch_snippets(snippets, sentences_per_timestamp_group=1)
    assert text == "[00:00 (0.0s)] This is a test. [00:05 (5.0s)] Snippet three!"
