"""Getters."""

from yt_summary.schemas.enums import SummarisationModesEnum
from yt_summary.summarisers.base_summariser import BaseSummariser
from yt_summary.summarisers.simple_summariser import SimpleSummariser
from yt_summary.summarisers.timestamp_summariser import RefinedSummariser

summarisers: dict[SummarisationModesEnum, type[BaseSummariser]] = {
    SummarisationModesEnum.SIMPLE: SimpleSummariser,
    SummarisationModesEnum.REFINE: RefinedSummariser,
}
