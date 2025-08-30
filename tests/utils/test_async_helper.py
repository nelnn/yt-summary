import time

import pytest

from src.utils.async_helpers import to_async


def blocking_func(a: int, b: int) -> int:
    time.sleep(1)
    return a + b


@pytest.mark.asyncio
async def test_to_async():
    result = await to_async(blocking_func, 2, 3)
    assert result == 5
