import logging
from typing import Type

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.metrics.api.prometheus import received_coordinates, \
    speed_violations, altitude_anomalies, unique_drivers
from adapters.repository.postgresql.drivers_repository import DriversRepository
from domain.entities import DriverInfo
from domain.repository.repository import ABCDriversRepository


class SaveDriverInfoUseCase:
    _repository: Type[ABCDriversRepository] = DriversRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    async def execute(self, driver_info: DriverInfo) -> int:
        try:
            async with self._session.begin():
                repository = self._repository(session=self._session)
                last_driver_info = await repository.get(driver_info.driver_id)
                if not driver_info.is_valid_speed():
                    logging.info(
                        f"Driver {driver_info.driver_id} has no valid speed"
                    )
                    speed_violations.inc()

                elif not driver_info.is_valid_altitude():
                    logging.info(
                        f"Driver {driver_info.driver_id} has no valid altitude"
                    )
                    altitude_anomalies.inc()

                elif not driver_info.is_valid_distance(last_driver_info):
                    logging.info(
                        f"Driver {driver_info.driver_id} has no valid distance"
                    )

                else:
                    driver_info.is_correct = True

                record_id = await repository.create(driver_info)
                await self._session.flush()
                received_coordinates.inc()
                unique_drivers_ids = await repository.get_unique_driver_ids()
                unique_drivers.set(unique_drivers_ids)
                await self._session.commit()
                logging.info(f"Driver {driver_info.driver_id} info successfully saved {record_id=}")  # noqa E501
                return record_id

        except (sqlalchemy.exc.InterfaceError, ConnectionError):
            raise ConnectionError

        except Exception as e:
            await self._session.rollback()
            raise e
