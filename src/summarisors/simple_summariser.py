"""High level summary."""

from llama_index.core import Document, DocumentSummaryIndex, PromptTemplate, get_response_synthesizer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.response_synthesizers.type import ResponseMode

from src.schemas.models import YoutubeTranscriptRaw
from src.summarisors.base_summariser import BaseSummariser
from src.summarisors.templates import SIMPLE_SUMMARY_QA_PROMPT_TEMPLATE


class SimpleSummariser(BaseSummariser):
    """Class for generating high level summaries from video transcripts."""

    async def summarise(self, transcript: YoutubeTranscriptRaw) -> str:
        """Generate a high level summary from the provided text.

        Args:
            transcript: The transcript to summarise.

        Returns:
            A high level summary of the transcript.

        """
        docs = Document(
            text=transcript.text, metadata=transcript.metadata.model_dump(), doc_id=transcript.metadata.video_id
        )
        splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
        response_synthesizer = get_response_synthesizer(
            llm=self.model,
            text_qa_template=PromptTemplate(SIMPLE_SUMMARY_QA_PROMPT_TEMPLATE),
            response_mode=ResponseMode.COMPACT,
            use_async=True,
        )
        index = DocumentSummaryIndex.from_documents(
            [docs],
            llm=self.model,
            transformations=[splitter],
            response_synthesizer=response_synthesizer,
            show_progress=True,
        )
        return index.get_document_summary(transcript.metadata.video_id)
