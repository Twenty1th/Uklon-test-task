from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

ENGINE = create_async_engine(
    "postgresql+asyncpg://postgres:password@127.0.0.1:5433",
    pool_size=5,
    echo_pool=False,  # todo
    echo=False  # todo
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
