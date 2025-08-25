"""Transcipt Endpoints."""

from typing import Annotated

import asyncpg
import fastapi
from fastapi import Depends, Query
from youtube_transcript_api import YouTubeTranscriptApi

from src.config import db_conn
from src.database.inserts.transcript import InsertYTMetadata

router = fastapi.APIRouter(tags=["transcript"], prefix="/transcript")


@router.get("/{video_id}", status_code=fastapi.status.HTTP_200_OK)
async def get_transcript(
    video_id: str,
    languages: Annotated[str | list[str], Query(...)] | None = None,
    conn: asyncpg.Connection = Depends(db_conn),
) -> None:
    """Get transcript.

    Args:
        video_id: YouTube video ID.
        languages: A list of language codes in a descending priority.
        conn: Database connection.

    """
    if isinstance(languages, str):
        languages = [languages]
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=languages or ["en"])
    stmt = InsertYTMetadata(
        video_id=video_id,
        language=transcript.language.split(" ")[0],
        language_code=transcript.language_code,
        is_generated=transcript.is_generated,
    )
    await conn.execute(stmt.template, *stmt.params)

    # TODO: Load to vector database
    # Return something
