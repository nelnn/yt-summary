"""Command line interface for the YouTube summary tool."""

import argparse
import os
import sys
from importlib.metadata import PackageNotFoundError, version

from src.schemas.enums import SummarisationModeEnum


class YTSummaryCLI:
    """Command line interface for the YouTube summary tool."""

    def __init__(self, args: list[str]) -> None:
        self._args = args

    async def run(self) -> str:
        """Run the CLI tool."""
        parsed_args = self._parse_args()

        if not parsed_args.url:
            return "Please provide a YouTube video URL or ID."

        from src.schemas.enums import LLMEnum

        if parsed_args.provider not in LLMEnum:
            return f"Unsupported provider: {parsed_args.provider}. Supported providers: {[e.value for e in LLMEnum]}"

        from src.llm_config import llm_configs

        llm_config = llm_configs[parsed_args.provider]
        if not os.getenv(llm_config.key_name) and not llm_config.default_key:
            return f"{llm_config.key_name} environment variable not set."

        try:
            from src.extractors.transcript import TranscriptExtractor
            from src.run.getters import summariser_dict
            from src.schemas.models import LLMModel

            transcript_extractor = TranscriptExtractor()
            text = await transcript_extractor.fetch(parsed_args.url)

            llm_model = LLMModel(
                provider=parsed_args.provider,
                model=parsed_args.model or llm_config.default_model,
            )
            summariser = summariser_dict[parsed_args.mode](llm=llm_model)
            summary = await summariser.summarise(text)

            if parsed_args.output:
                if not any(parsed_args.output.endswith(ext) for ext in {".txt", ".md", ".html"}):
                    return "Output file must have a valid extension (.txt, .md, .html)"

                import aiofiles

                async with aiofiles.open(parsed_args.output, "w", encoding="utf-8") as f:
                    await f.write(summary)

            return summary

        except Exception as e:  # noqa: BLE001
            return str(e)

    def _get_version(self) -> str:
        try:
            return version("yt-summary")
        except PackageNotFoundError:
            return "unknown"

    def _parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Summarize a YouTube video's transcript.")
        parser.add_argument(
            "url",
            type=str,
            help=("The video ID or URL of the Youtube video to summarize. Use quotes if URL is passed."),
        )

        # TODO: no metadata found error
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
            help="Language model provider to use (default: openai).",
        )

        parser.add_argument(
            "--model",
            "-m",
            type=str,
            default=None,
            help="Language model to use (default: gpt-5-mini-2025-08-07).",
        )

        parser.add_argument(
            "--mode",
            type=SummarisationModeEnum,
            default="simple",
            help="Summarization mode: simple or detailed (default: simple).",
        )

        parser.add_argument(
            "--output",
            "-o",
            default=os.getcwd(),
            help="Save summary as text/markdown/html",
        )

        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)

        return parser.parse_args(self._args)
