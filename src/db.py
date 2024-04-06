import os
import asyncpg
from src.config import settings


async def get_db():
    try:
        conn_pool = await asyncpg.create_pool(database=settings.DB_NAME, user=settings.DB_USER,
                                              port=settings.DB_PORT, host=settings.DB_HOSTNAME,
                                              password=settings.DB_PASSWORD)
        yield conn_pool
        await conn_pool.close()

    except Exception:
        raise 'Failed to connect to the database'

