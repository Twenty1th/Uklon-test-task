from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repository.postgresql import get_session
from domain.use_cases import SaveDriverInfoUseCase


async def save_driver_info_use_case(
        session: Annotated[AsyncSession, Depends(get_session)],
) -> SaveDriverInfoUseCase:
    yield SaveDriverInfoUseCase(session=session)

