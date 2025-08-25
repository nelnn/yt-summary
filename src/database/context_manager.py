from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg


@asynccontextmanager
async def db_engine(conn_str: str) -> AsyncGenerator[asyncpg.Connection, None]:
    """Asynchronous context manager for database connection.

    Yields:
        AsyncGenerator[asyncpg.Connection, None]: An asyncpg connection object.

    """
    conn = await asyncpg.connect(conn_str)
    try:
        yield conn
    finally:
        await conn.close()


class DBSession:
    """Asynchronous database session manager.

    Attributes:
        conn_str (str): The connection string for the database.

    """

    def __init__(self, conn_str: str) -> None:
        self.conn_str = conn_str

    async def __call__(self) -> AsyncGenerator[asyncpg.Connection, None]:
        conn = await asyncpg.connect(self.conn_str)
        try:
            yield conn
        finally:
            await conn.close()
