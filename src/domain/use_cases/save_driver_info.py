from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repository.postgresql.drivers_repository import DriversRepository
from domain.entities import DriverInfo
from domain.repository.repository import ABCDriversRepository


class GetPreviewDriverInfo:
    _repository: Type[ABCDriversRepository] = DriversRepository

    def __init__(self, session: AsyncSession):
        self._session = session


class SaveDriverInfoUseCase:
    _repository: Type[ABCDriversRepository] = DriversRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    async def execute(self, driver_info: DriverInfo) -> int:

        async with self._session.begin():
            repository = self._repository(session=self._session)
            try:
                last_driver_info = await repository.get(driver_info.driver_id)
                if last_driver_info is None:
                    driver_info.is_correct = True
                elif all([
                    driver_info.is_valid(),
                    driver_info.is_valid_distance(last_driver_info),
                ]):
                    driver_info.is_correct = True
                record_id = await repository.create(driver_info)
                await self._session.commit()
                return record_id

            except Exception as e:
                await self._session.rollback()
                raise e
