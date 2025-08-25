"""Extract metadata from YouTube videos using yt-dlp."""

from datetime import datetime

import yt_dlp

from src.schemas.models import YoutubeMetadata


def extract_metadata(url: str) -> YoutubeMetadata:
    """Extract metadata from a YouTube video URL.

    Args:
        url: The YouTube video URL.

    Returns:
        A tuple containing the YoutubeMetadata object and subtitles dictionary (if available).

    Raises:
        ValueError: If no metadata is found.

    """
    opts = {"quiet": True, "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    if isinstance(info, dict):
        return YoutubeMetadata(
            video_id=info["id"],
            title=info["title"],
            description=info["description"],
            uploader=info["uploader"],
            uploader_id=info["uploader_id"],
            channel=info["channel"],
            channel_id=info["channel_id"],
            upload_date=datetime.strptime(info["upload_date"], "%Y%m%d").date(),
            duration=info["duration"],
            webpage_url=info["webpage_url"],
            language=info.get("language"),
        )
    raise ValueError("Video not found")
