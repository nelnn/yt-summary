"""Timestamped summariser module."""

import asyncio

from llama_index.core.node_parser import SentenceSplitter

from yt_summary.schemas.models import YoutubeTranscriptRaw
from yt_summary.summarisers.base_summariser import BaseSummariser
from yt_summary.summarisers.templates import TIMESTAMPED_CONSOLIDATION_PROMPT, TIMESTAMPED_SUMMARY_CHUCKED_PROMPT


class RefinedSummariser(BaseSummariser):
    """Class for generating refined timestamped summaries from video transcripts."""

    async def summarise(self, transcript: YoutubeTranscriptRaw) -> str:
        """Generate a timestamped summary from the provided text.

        Args:
            transcript: The transcript to summarise.

        Returns:
            A timestamped summary of the transcript.

        """
        chunks = SentenceSplitter(chunk_size=4096, chunk_overlap=200).split_text(transcript.text)
        tasks = [self.model.llm.acomplete(TIMESTAMPED_SUMMARY_CHUCKED_PROMPT.format(chunk=chunk)) for chunk in chunks]
        section_texts = "\n".join([s.text.strip() for s in await asyncio.gather(*tasks)])
        final_response = await self.model.llm.acomplete(
            TIMESTAMPED_CONSOLIDATION_PROMPT.format(combined_summary=section_texts)
        )
        return final_response.text
