import logging

import sqlalchemy
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

import settings

ENGINE = create_async_engine(
    settings.CONFIG.pgsql.postgres_url,
    pool_size=settings.CONFIG.pgsql.postgres_pool_size,
    echo_pool=settings.CONFIG.pgsql.postgres_echo,
    echo=settings.CONFIG.pgsql.postgres_echo,
)
async_session_factory = async_sessionmaker(
    ENGINE,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)


async def database_is_alive():
    async with async_session_factory() as session:  # type: AsyncSession
        try:
            await session.execute(text("SELECT 1"))
            return True

        except (sqlalchemy.exc.InterfaceError, ConnectionRefusedError):
            logging.error("Failed to connect to database")
            return False
