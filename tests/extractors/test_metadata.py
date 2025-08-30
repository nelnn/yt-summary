from unittest.mock import patch

import aiohttp
import pytest
from aioresponses import aioresponses

from src.extractors.metadata import extract_metadata
from src.schemas.exceptions import MetadataNotFoundError
from src.schemas.models import YoutubeMetadata


@pytest.mark.asyncio
async def test_extract_metadata():
    url = "https://www.youtube.com/watch?v=dQw4w9W"

    mock_response = {
        "title": "foo",
        "author_name": "bar",
        "author_url": "https://www.youtube.com/channel/@baz",
        "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9W/hqdefault.jpg",
    }

    with aioresponses() as m:
        m.get(f"https://www.youtube.com/oembed?url={url}&format=json", payload=mock_response)

        metadata = await extract_metadata(url)

        assert isinstance(metadata, YoutubeMetadata)
        assert metadata.video_id == "dQw4w9W"
        assert metadata.title == "foo"
        assert metadata.author == "bar"
        assert metadata.channel_id == "baz"
        assert str(metadata.thumbnail_url) == "https://i.ytimg.com/vi/dQw4w9W/hqdefault.jpg"


@pytest.mark.asyncio
async def test_extract_metadata_failure():
    test_url = "https://www.youtube.com/watch?v=failure123"
    with patch("aiohttp.ClientSession.get", side_effect=aiohttp.ClientError("Mocked connection error")):
        with pytest.raises(MetadataNotFoundError) as exc_info:
            await extract_metadata(test_url)
