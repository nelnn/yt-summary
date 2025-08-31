"""Miscellaneous utility functions."""

import time


def convert_to_readable_time(seconds: int) -> str:
    """Convert seconds to a human-readable time format (hh:mm:ss or mm:ss).

    Args:
        seconds (int): The number of seconds to convert.

    Returns:
        str: The time in hh:mm:ss format if >= 1 hour, otherwise mm:ss format.

    """
    if seconds >= 3600:
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
    return time.strftime("%M:%S", time.gmtime(seconds))
