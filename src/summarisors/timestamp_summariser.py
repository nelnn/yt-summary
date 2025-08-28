"""Timestamped summariser module."""

import asyncio

from llama_index.core.node_parser import SentenceSplitter

from src.summarisors.base_summariser import BaseSummariser
from src.summarisors.templates import TIMESTAMPED_CONSOLIDATION_PROMPT, TIMESTAMPED_SUMMARY_CHUCKED_PROMPT


class TimestampedSummariser(BaseSummariser):
    """Class for generating timestamped summaries from video transcripts."""

    async def summarise(self, text: str) -> str:
        """Generate a timestamped summary from the provided text.

        Args:
            text: The transcript text to summarise.

        Returns:
            A timestamped summary of the transcript.

        """
        chunks = SentenceSplitter(chunk_size=4096, chunk_overlap=200).split_text(text)
        tasks = [self.model.acomplete(TIMESTAMPED_SUMMARY_CHUCKED_PROMPT.format(chunk=chunk)) for chunk in chunks]
        section_texts = "\n".join([s.text.strip() for s in await asyncio.gather(*tasks)])
        final_response = await self.model.acomplete(
            TIMESTAMPED_CONSOLIDATION_PROMPT.format(combined_summary=section_texts)
        )
        return final_response.text
