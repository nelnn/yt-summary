"""Prompt templates for video summarization tasks."""

TIMESTAMPED_SUMMARY_CHUCKED_PROMPT = """
    You are given a portion of a youtube transcript with timestamps labeled as <<t=timestamp>>.
    Create a summary of the key points in this section with their corresponding timestamps.
    Since each timestamp represents a less than or equal to one coherent sentence,
    you should group multiple timestamps together if they relate to the same key point,
    and use the earliest timestamp for that point.

    FORMATTING RULES:
    - Extract timestamps from <<t=timestamp>> markers
    - Format each point as: [timestamp] Summary text
    - Focus on main topics, arguments, and examples
    - Be concise but comprehensive
    - Only include the start timestamp for each key point in seconds
    - Ignore sponsor blocks

    Transcript section:
        {chunk}

    Here is the timestamped summary of key points from this section:
"""


TIMESTAMPED_CONSOLIDATION_PROMPT = """
    You are given multiple timestamped summaries from different sections of a video transcript which are overlaped.
    Organize and consolidate these into a coherent, comprehensive summary.

    RULES:
    - First give an overall summary of the transcript in one to two paragraphs.
    - Consolidate the timestamps and key points. If successive sections relate to the same key point,
        merge them into a single point with the earliest timestamp.
    - Remove any redundancy
    - Maintain chronological order
    - Format as: [timestamp] Summary text
    - You can group the key points under thematic headings if it improves clarity.
    - You can ignore the chronological order if it improves clarity. For example, if a topic is discussed at
        multiple points in the transcript, you can group those points together. and provide the timestamps in
        the format [timestamp1, timestamp2, ...] Summary text

    Section summaries:
        {combined_summary}

    Here is the high level summary as well as the timestamped summary of key points:
    """


SIMPLE_SUMMARY_QA_PROMPT_TEMPLATE = """
    You are an expert summarizer and question answerer.
    Given the following document, give the metadata of the video such as title and author and
    generate a concise, high-level summary.
    After the summary, generate a list of insightful questions that this document can answer,
    and provide brief, accurate answers to each.
    There's no need prompt the user to ask questions, as this is a self-contained summary and Q&A.

    RULES:
        - Give the Youtube metada at the top.
        - The QA format should be:
            (optional) Timestamps:
                - timestamp 1 - summary point 1
                - timestamp 2 - summary point 2
            Q: Question? [timestamp1, timestamp2, ...]
            A: Answer. [timestamp1, timestamp2, ...]

    Document:\n{context_str}\n\n

    Here is the video information and the summary with Q&A:\n
"""
