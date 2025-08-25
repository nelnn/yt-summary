import asyncio
from pathlib import Path

import aiofiles

from src.config import engine, settings


async def run_migrations() -> None:
    """Run migration.

    Only runs the last migration file found in the migrations folder.
    """
    paths = Path(settings.MIGRATIONS_FOLDER_PATH).glob("*.sql")
    file = sorted(x for x in paths if x.is_file())[0]

    async with aiofiles.open(file, "r") as f:
        sql = await f.read()
        async with engine as conn:
            await conn.execute(sql)


asyncio.run(run_migrations())
