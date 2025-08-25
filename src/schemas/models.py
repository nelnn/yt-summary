from datetime import date

from pydantic import BaseModel


class YoutubeMetadata(BaseModel):
    """YouTube video metadata model."""

    video_id: str
    title: str
    description: str
    uploader: str
    uploader_id: str
    channel: str
    channel_id: str
    upload_date: date
    duration: int
    webpage_url: str
    language: str | None = None
