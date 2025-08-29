"""Entry point for the CLI."""

import asyncio
import logging
import sys
import time

from src.cli.cli import YTSummaryCLI

start = time.perf_counter()


async def main() -> None:
    """Run the CLI tool."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )
    logger = logging.getLogger("yt-summary")
    logger.info(await YTSummaryCLI(sys.argv[1:]).run())


if __name__ == "__main__":
    asyncio.run(main())
