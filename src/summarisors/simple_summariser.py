"""High level summary."""

import nest_asyncio
from llama_index.core import Document, DocumentSummaryIndex, get_response_synthesizer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.response_synthesizers.type import ResponseMode

from src.summarisors.base_summariser import BaseSummariser

nest_asyncio.apply()


class SimpleSummariser(BaseSummariser):
    """Class for generating high level summaries from video transcripts."""

    async def summarise(self, text: str) -> str:
        """Generate a high level summary from the provided text.

        Args:
            text: The transcript text to summarise.

        Returns:
            A high level summary of the transcript.

        """
        docs = Document(text=text, doc_id="video")
        splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
        response_synthesizer = get_response_synthesizer(
            llm=self.model,
            response_mode=ResponseMode.TREE_SUMMARIZE,
            use_async=True,
        )
        doc_summary_index = DocumentSummaryIndex.from_documents(
            [docs],
            llm=self.model,
            transformations=[splitter],
            response_synthesizer=response_synthesizer,
            show_progress=True,
        )
        return doc_summary_index.get_document_summary("video")


if __name__ == "__main__":
    import asyncio

    from src.extractors.transcript import TranscriptExtractor
    from src.schemas.enums import LLMEnum

    e = TranscriptExtractor()
    text = asyncio.run(e.fetch("https://www.youtube.com/watch?v=VbNF9X1waSc"))
    s = SimpleSummariser(model=LLMEnum.GOOGLE)
    summary = s.summarise(text.transcript)
