"""Getters."""

from src.schemas.enums import SummarisationModeEnum
from src.summarisors.base_summariser import BaseSummariser
from src.summarisors.simple_summariser import SimpleSummariser
from src.summarisors.timestamp_summariser import TimestampedSummariser

summariser_dict: dict[SummarisationModeEnum, type[BaseSummariser]] = {
    SummarisationModeEnum.SIMPLE: SimpleSummariser,
    SummarisationModeEnum.DETAILED: TimestampedSummariser,
}
