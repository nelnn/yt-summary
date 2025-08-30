"""Custom argparse type for LLMProvidersEnum validation."""

import argparse

from src.schemas.enums import LLMProvidersEnum


def provider_type(provider: str) -> LLMProvidersEnum:
    """Ensure the provider argument is a valid LLMProvidersEnum value.

    Args:
        provider (str): The provider string to validate.

    Returns:
        LLMProvidersEnum: The corresponding LLMProvidersEnum value.

    Raises:
        argparse.ArgumentTypeError: If the provider is not valid.

    """
    try:
        return LLMProvidersEnum(provider)
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid provider '{provider}'. Must be one of: {[p.value for p in LLMProvidersEnum]}"
        ) from e
