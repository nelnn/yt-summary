import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Awaitable, Callable

executor = ThreadPoolExecutor()


async def to_async(func: Callable[..., Any], *args: Any, **kwargs: dict[str, Any]) -> Awaitable[Callable[..., Any]]:
    """Run a blocking function in an async context using ThreadPoolExecutor."""
    loop = asyncio.get_event_loop()
    with executor as pool:
        return await loop.run_in_executor(pool, func, *args, **kwargs)
