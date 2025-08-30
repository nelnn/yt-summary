from unittest.mock import AsyncMock, patch

import aiohttp
import pytest

from src.extractors.metadata import extract_metadata
from src.schemas.exceptions import MetadataNotFoundError
from src.schemas.models import YoutubeMetadata


@pytest.mark.asyncio
async def test_extract_metadata(fake_youtube_metadata_json):
    url = "https://www.youtube.com/watch?v=dQw4w9W"

    mock_response = AsyncMock()
    mock_response.__aenter__.return_value = mock_response
    mock_response.json.return_value = fake_youtube_metadata_json

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        metadata = await extract_metadata(url)
        assert isinstance(metadata, YoutubeMetadata)


@pytest.mark.asyncio
async def test_extract_metadata_failure():
    test_url = "https://www.youtube.com/watch?v=failure123"
    with patch("aiohttp.ClientSession.get", side_effect=aiohttp.ClientError("Mocked connection error")):
        with pytest.raises(MetadataNotFoundError):
            await extract_metadata(test_url)
