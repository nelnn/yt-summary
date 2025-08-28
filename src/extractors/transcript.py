"""Fetch transcript."""

import asyncio
from typing import Iterable

from requests import Session
from youtube_transcript_api import FetchedTranscript, YouTubeTranscriptApi
from youtube_transcript_api.proxies import ProxyConfig

from src.extractors.metadata import extract_metadata
from src.schemas.models import YoutubeTranscriptRaw
from src.utils.async_helpers import to_async


class TranscriptExtractor:
    """Transcript extractor. A wrapper around YouTubeTranscriptApi.

    Attributes:
        video_id: video id
        ytt_api: YouTubeTranscriptApi instance
        _transcript: fetched transcript

    """

    def __init__(self, proxy_config: ProxyConfig | None = None, http_client: Session | None = None) -> None:
        self.ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config, http_client=http_client)
        self._transcript = None

    @property
    def transcript(self) -> FetchedTranscript | None:
        """Get transcript."""
        return self._transcript

    async def fetch(
        self, url: str, languages: Iterable[str] | None = None, *, preserve_formatting: bool = False
    ) -> YoutubeTranscriptRaw:
        """Asynchronously fetch transcript.

        Args:
            url: video URL or ID you want to retrieve the transcript for.
            languages: A list of language codes in a descending priority. For
                example, if this is set to ["de", "en"] it will first try to fetch the
                german transcript (de) and then fetch the english transcript (en) if
                it fails to do so. This defaults to ["en"].
            preserve_formatting: whether to keep select HTML text formatting

        Returns:
            The transcript text.

        """
        transcript, metadata = await asyncio.gather(
            self._afetch_transcript(
                url,
                languages=languages,
                preserve_formatting=preserve_formatting,
            ),
            extract_metadata(url),
        )

        return YoutubeTranscriptRaw(metadata=metadata, transcript=transcript)

    def fetch_transcript(
        self, url: str, languages: Iterable[str] | None = None, *, preserve_formatting: bool = False
    ) -> str:
        """Fetch transcript.

        Args:
            url: video URL or ID you want to retrieve the transcript for.
            languages: A list of language codes in a descending priority. For
                example, if this is set to ["de", "en"] it will first try to fetch the
                german transcript (de) and then fetch the english transcript (en) if
                it fails to do so. This defaults to ["en"].
            preserve_formatting: whether to keep select HTML text formatting

        Returns:
            The transcript text.

        """
        video_id = url.split("?v=")[-1].split("&")[0]
        if not languages:
            languages = ["en"]
        if not self._transcript:
            self._transcript = self.ytt_api.fetch(
                video_id,
                languages=languages,
                preserve_formatting=preserve_formatting,
            )
        texts = [snippet.text + f" <<t={int(snippet.start)}>>\n" for snippet in self._transcript.snippets]
        return " ".join(texts)

    async def _afetch_transcript(
        self, url: str, languages: Iterable[str] | None = None, *, preserve_formatting: bool = False
    ) -> str:
        """Asynchronously fetch transcript.

        Args:
            url: video URL or ID you want to retrieve the transcript for.
            languages: A list of language codes in a descending priority. For
                example, if this is set to ["de", "en"] it will first try to fetch the
                german transcript (de) and then fetch the english transcript (en) if
                it fails to do so. This defaults to ["en"].
            preserve_formatting: whether to keep select HTML text formatting

        Returns:
            The transcript text.

        """
        kwargs = {
            "url": url,
            "languages": languages,
            "preserve_formatting": preserve_formatting,
        }
        return await to_async(self.fetch_transcript, **kwargs)
