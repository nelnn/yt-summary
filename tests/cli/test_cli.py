import argparse
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.cli import YTSummaryCLI
from src.schemas.enums import SummarisationModeEnum


class TestYTSummaryCLI:
    def test_parse_args_minimal(self):
        cli = YTSummaryCLI(["https://youtube.com/watch?v=abc123"])
        args = cli._parse_args()
        assert args.url == "https://youtube.com/watch?v=abc123"
        assert args.provider == "openai"
        assert args.model is None
        assert args.mode == SummarisationModeEnum.SIMPLE
        assert args.output is None

    def test_parse_args_with_all_flags(self):
        cli = YTSummaryCLI(
            [
                "abc123",
                "--provider",
                "openai",
                "--model",
                "gpt-5-mini",
                "--mode",
                "detailed",
                "--output",
                "summary.txt",
            ]
        )
        args = cli._parse_args()
        assert args.url == "abc123"
        assert args.provider == "openai"
        assert args.model == "gpt-5-mini"
        assert args.mode == SummarisationModeEnum.DETAILED
        assert args.output == "summary.txt"

    def test_parse_args_fails_without_args(self, monkeypatch):
        cli = YTSummaryCLI([])
        monkeypatch.setattr(sys, "argv", ["yt-summary"])
        with pytest.raises(SystemExit):
            cli._parse_args()

    def test_get_version_package_not_found(self):
        cli = YTSummaryCLI([])
        with patch("src.cli.cli.version", side_effect=Exception):
            assert cli._get_version() in {"unknown"}

    @pytest.mark.asyncio
    async def test_run_missing_url(self):
        cli = YTSummaryCLI([])
        with patch.object(cli, "_parse_args", return_value=argparse.Namespace(url=None)):
            result = await cli.run()
            assert "Please provide a YouTube video URL" in result

    @pytest.mark.asyncio
    async def test_run_unsupported_provider(self):
        cli = YTSummaryCLI([])
        args = argparse.Namespace(
            url="abc123",
            provider="fake",
            model=None,
            mode="simple",
            output=None,
        )
        with patch.object(cli, "_parse_args", return_value=args):
            result = await cli.run()
            assert "Unsupported provider" in result

    @pytest.mark.asyncio
    async def test_run_missing_env_var(self):
        cli = YTSummaryCLI([])
        args = argparse.Namespace(
            url="abc123",
            provider="openai",
            model=None,
            mode="simple",
            output=None,
        )

        # Fake LLMEnum membership
        with (
            patch("src.schemas.enums.LLMEnum", ["openai"]),
            patch("src.llm_config.llm_configs", {"openai": MagicMock(key_name="OPENAI_API_KEY", default_key=None)}),
            patch.dict(os.environ, {}, clear=True),
            patch.object(cli, "_parse_args", return_value=args),
        ):
            result = await cli.run()
            assert "OPENAI_API_KEY environment variable not set" in result

    @patch.object(YTSummaryCLI, "_parse_args")
    @pytest.mark.asyncio
    async def test_run_successful_summary(mock_parse_args, tmp_path):
        cli = YTSummaryCLI([])
        args = argparse.Namespace(
            url="abc123",
            provider="openai",
            model=None,
            mode="simple",
            output=str(tmp_path / "out.txt"),
        )
        mock_parse_args.return_value = args

        fake_llm_config = MagicMock(key_name="OPENAI_API_KEY", default_key="dummy", default_model="gpt-5")
        fake_transcript_text = "This is a transcript."
        fake_summary = "This is a summary."

        with (
            patch("src.llm_config.llm_configs", {"openai": fake_llm_config}),
            patch.dict(os.environ, {"OPENAI_API_KEY": "x"}),
            patch(
                "src.extractors.transcript.TranscriptExtractor",
                return_value=MagicMock(fetch=AsyncMock(return_value=fake_transcript_text)),
            ),
            patch(
                "src.run.getters.summariser_dict",
                {"simple": lambda llm: MagicMock(summarise=AsyncMock(return_value=fake_summary))},
            ),
            patch("src.schemas.models.LLMModel"),
        ):
            with patch("aiofiles.open", new_callable=AsyncMock) as mock_aiofiles:
                result = await cli.run()

        assert result == fake_summary

    @pytest.mark.asyncio
    async def test_run_invalid_output_extension(self):
        cli = YTSummaryCLI([])
        args = argparse.Namespace(
            url="abc123",
            provider="openai",
            model=None,
            mode="simple",
            output="badfile.pdf",
        )

        with (
            patch("src.schemas.enums.LLMEnum", ["openai"]),
            patch(
                "src.llm_config.llm_configs",
                {"openai": MagicMock(key_name="OPENAI_API_KEY", default_key="dummy", default_model="gpt-5")},
            ),
            patch.dict(os.environ, {"OPENAI_API_KEY": "x"}),
            patch(
                "src.extractors.transcript.TranscriptExtractor",
                return_value=MagicMock(fetch=AsyncMock(return_value="text")),
            ),
            patch(
                "src.run.getters.summariser_dict",
                {"simple": lambda llm: MagicMock(summarise=AsyncMock(return_value="summary"))},
            ),
            patch("src.schemas.models.LLMModel"),
        ):
            result = await cli.run()
            assert "Output file must have a valid extension" in result

    @pytest.mark.asyncio
    async def test_run_exception_handling(self):
        cli = YTSummaryCLI([])
        args = argparse.Namespace(
            url="abc123",
            provider="openai",
            model=None,
            mode="simple",
            output=None,
        )

        with (
            patch("src.schemas.enums.LLMEnum", ["openai"]),
            patch(
                "src.llm_config.llm_configs",
                {"openai": MagicMock(key_name="OPENAI_API_KEY", default_key="dummy", default_model="gpt-5")},
            ),
            patch.dict(os.environ, {"OPENAI_API_KEY": "x"}),
            patch("src.extractors.transcript.TranscriptExtractor", side_effect=RuntimeError("boom")),
            patch("src.run.getters.summariser_dict", {}),
            patch("src.schemas.models.LLMModel"),
        ):
            result = await cli.run()
            assert "boom" in result
