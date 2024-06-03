import asyncpg

from lucy import settings

__pool = None


async def initialize_pool(*, min_size=2, max_size=40):
    global __pool
    __pool = await asyncpg.create_pool(
        host=settings.DB_HOST,
        database=settings.DB_NAME,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        timeout=5,
        min_size=min_size,
        max_size=max_size,
    )


def get_pool() -> asyncpg.Pool:
    assert __pool, 'pool uninitialized, call initialize_pool first'
    return __pool
