"""Getters."""

from src.schemas.enums import SummarisationModeEnum
from src.summarisers.base_summariser import BaseSummariser
from src.summarisers.simple_summariser import SimpleSummariser
from src.summarisers.timestamp_summariser import TimestampedSummariser

summarisers: dict[SummarisationModeEnum, type[BaseSummariser]] = {
    SummarisationModeEnum.SIMPLE: SimpleSummariser,
    SummarisationModeEnum.REFINE: TimestampedSummariser,
}
