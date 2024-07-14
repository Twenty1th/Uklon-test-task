import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from adapters.metrics.api.prometheus import db_writes
from adapters.repository.postgresql import database_is_alive
from application.api.v1.depends import get_session
from domain.entities import DriverInfo
from domain.use_cases import SaveDriverInfoUseCase
from domain.use_cases.drivers import GetLastDriverInfo


class FallBackQueue(asyncio.Queue[DriverInfo]):

    async def get(self) -> DriverInfo:
        driver_info: DriverInfo = await super().get()
        self.task_done()
        return driver_info

    async def dump(self) -> None:
        while not self.empty():
            try:
                if not await database_is_alive():
                    raise ConnectionError

                async for session in get_session():  # type: AsyncSession
                    driver_info = await self.get()
                    save_use_case = SaveDriverInfoUseCase(session=session)
                    get_last_driver_info = GetLastDriverInfo(session=session)
                    last_driver_info = await get_last_driver_info.execute(driver_id=driver_info.driver_id)
                    if last_driver_info and not driver_info.is_valid_distance(last_driver_info):
                        logging.info(
                            f"[Driver {driver_info.driver_id}]: has no valid distance"
                        )
                        driver_info.is_correct = False

                    await save_use_case.execute(driver_info)
                    logging.info(f"[Driver info {driver_info.driver_id}]: dumped from fallback queue")

                    # Increase db writes metrics
                    db_writes.inc()

            except asyncio.CancelledError:
                return

            except ConnectionError:
                logging.info("Database is not alive")
                return

            except Exception as e:
                logging.error(e)
                return
