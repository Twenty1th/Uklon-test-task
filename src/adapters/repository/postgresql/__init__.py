from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

ENGINE = create_async_engine(
    settings.CONFIG.postgres_url,
    pool_size=settings.CONFIG.postgres_pool_size,
    echo_pool=settings.CONFIG.postgres_echo,
    echo=settings.CONFIG.postgres_echo,
)
async_session_factory = sessionmaker(
    bind=ENGINE,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
