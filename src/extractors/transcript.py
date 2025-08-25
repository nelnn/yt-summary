"""Fetch transcript."""

from pathlib import Path

from youtube_transcript_api import FetchedTranscript, YouTubeTranscriptApi


class TranscriptExtractor:
    """Transcript extractor.

    Attributes:
        video_id: video id
        ytt_api: YouTubeTranscriptApi instance
        _transcript: fetched transcript

    """

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.ytt_api = YouTubeTranscriptApi()
        self._transcript = None

    @property
    def transcript(self) -> FetchedTranscript | None:
        """Get transcript."""
        return self._transcript

    def fetch_text(self, languages: list[str] | None = None) -> str:
        """Fetch transcript.

        Args:
            languages: A list of language codes in a descending priority. see
                YoutubeTranscriptApi.fetch for details.

        Returns:
            The transcript text.

        """
        if not languages:
            languages = ["en"]
        if not self._transcript:
            self._transcript = self.ytt_api.fetch(self.video_id, languages=languages)
        texts = [snippet.text + f" <<t={snippet.start}>>\n" for snippet in self._transcript.snippets]
        return " ".join(texts)

    def save_transcript(self, filename: str | Path) -> None:
        """Save transcript to file.

        Args:
            filename: filename to save the transcript

        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.fetch_text())


# e = TranscriptExtractor("AGglJehON5g")
# t = e.fetch_text()
# print(e.transcript)
# print(123)
