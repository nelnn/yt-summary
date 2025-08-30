"""Entry point for the CLI."""

import asyncio
import logging
import sys

from yt_summary.cli.cli import YTSummaryCLI


async def main() -> None:
    """Run the CLI tool."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )
    print(await YTSummaryCLI(sys.argv[1:]).run())


if __name__ == "__main__":
    asyncio.run(main())
