from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repository.postgresql import async_session_factory
from domain.use_cases import SaveDriverInfoUseCase
from domain.use_cases.drivers import GetLastDriverInfo, GetUniqueDriversUseCase


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def save_driver_info_use_case(
        session: Annotated[AsyncSession, Depends(get_session)],
) -> SaveDriverInfoUseCase:
    yield SaveDriverInfoUseCase(session=session)


async def get_last_driver_info_use_case(
        session: Annotated[AsyncSession, Depends(get_session)],
) -> GetLastDriverInfo:
    yield GetLastDriverInfo(session=session)


async def get_unique_drivers_use_case(
        session: Annotated[AsyncSession, Depends(get_session)],
) -> GetUniqueDriversUseCase:
    yield GetUniqueDriversUseCase(session=session)
