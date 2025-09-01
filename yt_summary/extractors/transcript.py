"""Fetch transcript."""

import asyncio
from typing import Iterable

from requests import Session
from youtube_transcript_api import FetchedTranscript, FetchedTranscriptSnippet, YouTubeTranscriptApi
from youtube_transcript_api.proxies import ProxyConfig

from yt_summary.extractors.metadata import extract_metadata
from yt_summary.schemas.models import YoutubeTranscriptRaw
from yt_summary.utils.async_helpers import to_async
from yt_summary.utils.misc import convert_to_readable_time


class TranscriptExtractor:
    """Transcript extractor. A wrapper around YouTubeTranscriptApi.

    Attributes:
        video_id: video id
        ytt_api: YouTubeTranscriptApi instance
        _transcript: fetched transcript

    """

    def __init__(self, proxy_config: ProxyConfig | None = None, http_client: Session | None = None) -> None:
        self.ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config, http_client=http_client)

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
        fetched_transcript, metadata = await asyncio.gather(
            self._afetch_transcript(
                url,
                languages=languages,
                preserve_formatting=preserve_formatting,
            ),
            extract_metadata(url),
        )
        text = self._stitch_snippets(fetched_transcript.snippets)
        metadata.is_generated = fetched_transcript.is_generated
        metadata.language = fetched_transcript.language
        metadata.language_code = fetched_transcript.language_code
        return YoutubeTranscriptRaw(
            metadata=metadata,
            text=text,
        )

    def fetch_transcript(
        self, url: str, languages: Iterable[str] | None = None, *, preserve_formatting: bool = False
    ) -> FetchedTranscript:
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
        return self.ytt_api.fetch(
            video_id,
            languages=languages if languages else ["en"],
            preserve_formatting=preserve_formatting,
        )

    async def _afetch_transcript(
        self, url: str, languages: Iterable[str] | None = None, *, preserve_formatting: bool = False
    ) -> FetchedTranscript:
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

    @staticmethod
    def _stitch_snippets(snippets: list[FetchedTranscriptSnippet], sentences_per_timestamp_group: int = 20) -> str:
        """Stitch snippets together and get the earliest timestamp.

        Args:
            snippets: list of transcript snippets
            sentences_per_timestamp_group: number of sentences to stitch together.

        Returns:
            stitched transcript.

        """
        text = []
        buffer = []
        start_time = None
        sentence_count = 0

        for i in range(len(snippets)):
            buffer.append(snippets[i].text)

            if start_time is None:
                start_time = int(snippets[i].start)

            if "." in snippets[i].text:
                sentence_count += 1

            if sentence_count == sentences_per_timestamp_group:
                stitched_text = " ".join(buffer)
                pos = stitched_text.rfind(".")
                text.append(f"[{convert_to_readable_time(start_time)} ({start_time}s)] {stitched_text[: pos + 1]} ")
                buffer = [stitched_text[pos + 1 :].strip()]
                sentence_count = 0
                start_time = None
            if i == len(snippets) - 1:
                text.append(
                    f"[{convert_to_readable_time(int(snippets[i - 1].start))} "
                    f"({int(snippets[i - 1].start)}s)] "
                    f"{' '.join(buffer)}"
                )
        return "".join(text).strip()
