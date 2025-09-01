"""Command line interface for the YouTube summary tool."""

import argparse
import os
import sys
from importlib.metadata import PackageNotFoundError, version


class YTSummaryCLI:
    """Command line interface for the YouTube summary tool."""

    def __init__(self, args: list[str]) -> None:
        self._args = args

    async def run(self) -> str:
        """Run the CLI tool."""
        parsed_args = self._parse_args()

        if not parsed_args.url:
            return "Please provide a YouTube video URL or ID."

        try:
            if parsed_args.mode:
                from yt_summary.cli.errors import check_mode_type

                check_mode_type(parsed_args.mode)

            if parsed_args.provider:
                from yt_summary.cli.errors import check_provider_type

                check_provider_type(parsed_args.provider)

            from yt_summary.llm_config import llm_configs

            llm_config = llm_configs[parsed_args.provider]

            if not os.getenv(llm_config.key_name):
                return f"{llm_config.key_name} environment variable not set."

            print(f"Provider: {parsed_args.provider.upper()} | Model: {parsed_args.model or llm_config.default_model}")

            from yt_summary.extractors.transcript import TranscriptExtractor
            from yt_summary.run.getters import summarisers
            from yt_summary.schemas.models import LLMModel

            llm_model = LLMModel(
                provider=parsed_args.provider,
                model=parsed_args.model or llm_config.default_model,
            )
            transcript_extractor = TranscriptExtractor()
            transcript = await transcript_extractor.fetch(parsed_args.url)
            summariser = summarisers[parsed_args.mode](llm=llm_model)
            return await summariser.summarise(transcript)

        except Exception as e:  # noqa: BLE001
            return str(e)

    def _get_version(self) -> str:
        try:
            return version("yt-summary")
        except PackageNotFoundError:
            return "unknown"

    def _parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(prog="yt-summary", description="Summarize a YouTube video's transcript.")
        parser.add_argument(
            "url",
            nargs="?",
            type=str,
            help=("The video ID or URL of the Youtube video to summarize. Use quotes if URL is passed."),
        )

        parser.add_argument(
            "--version",
            "-v",
            action="version",
            version=f"%(prog)s {self._get_version()}",
            help="Show the version number and exit.",
        )

        parser.add_argument(
            "--provider",
            "-p",
            type=str,
            default="openai",
            help="Language model provider to use. (default: openai)",
        )

        parser.add_argument(
            "--list-providers",
            action="store_true",
            help="List all supported language model providers.",
        )

        parser.add_argument(
            "--model",
            type=str,
            default=None,
            help="Model name for the provider.",
        )

        parser.add_argument(
            "--mode",
            "-m",
            type=str,
            default="simple",
            help="Summarization mode: `simple` or `refined` (default: simple).",
        )

        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)

        return parser.parse_args(self._args)
