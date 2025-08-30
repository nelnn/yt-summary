import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from yt_summary.cli.cli import YTSummaryCLI
from yt_summary.schemas.enums import LLMProvidersEnum, SummarisationModesEnum


@pytest.mark.asyncio
async def test_run_cli_no_url():
    cli = YTSummaryCLI(["--mode", "simple"])
    result = await cli.run()
    assert result == "Please provide a YouTube video URL or ID."


@pytest.mark.parametrize("provider", [provider.value for provider in LLMProvidersEnum])
def test_run_llm_provider(provider):
    cli = YTSummaryCLI(["www.foo.com", "--provider", provider])
    args = cli._parse_args()
    assert args.provider in [e.value for e in LLMProvidersEnum]


def test_run_llm_provider_invalid():
    cli = YTSummaryCLI(["www.foo.com", "--provider", "invalid"])
    with pytest.raises(SystemExit), pytest.raises(ValueError):
        cli._parse_args()


@pytest.mark.parametrize("mode", [mode.value for mode in SummarisationModesEnum])
def test_run_summarisation_mode(mode):
    cli = YTSummaryCLI(["www.foo.com", "--mode", mode])
    args = cli._parse_args()
    assert args.mode in [e.value for e in SummarisationModesEnum]


@pytest.mark.asyncio
async def test_run_cli_no_api_key():
    cli = YTSummaryCLI(["www.foo.com"])
    with patch.dict(os.environ, {}, clear=True):
        result = await cli.run()
        assert result == "OPENAI_API_KEY environment variable not set."


@pytest.mark.asyncio
async def test_run_cli_get_summary_success(mock_transcript, mock_summariser):
    cli = YTSummaryCLI(["www.foo.com"])
    mock_summariser_factory = MagicMock(return_value=mock_summariser)
    with (
        patch.dict(os.environ, {"OPENAI_API_KEY": "testkey"}),
        patch("yt_summary.extractors.transcript.TranscriptExtractor", return_value=mock_transcript),
        patch("yt_summary.run.getters.summarisers", {"simple": mock_summariser_factory}),
    ):
        result = await cli.run()
        assert result == "This is a summary."


@pytest.mark.asyncio
async def test_run_cli_exception_handling():
    cli = YTSummaryCLI(["www.foo.com"])

    mock_transcript = AsyncMock()
    mock_transcript.fetch.side_effect = Exception("Fetch failed")

    with (
        patch.dict(os.environ, {"OPENAI_API_KEY": "testkey"}),
        patch("yt_summary.extractors.transcript.TranscriptExtractor", return_value=mock_transcript),
    ):
        result = await cli.run()
        assert result == "Fetch failed"
