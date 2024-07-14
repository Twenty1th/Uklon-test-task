import logging
import socket
from typing import Type, Optional

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.metrics.api.prometheus import unique_drivers
from adapters.repository.postgresql.drivers_repository import DriversRepository
from domain.entities import DriverInfo
from domain.repository.repository import ABCDriversRepository


class GetLastDriverInfo:
    _repository: Type[ABCDriversRepository] = DriversRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    async def execute(self, driver_id: int) -> Optional[DriverInfo]:
        try:
            async with self._session.begin():
                repository = self._repository(session=self._session)
                return await repository.get(driver_id=driver_id)

        except (sqlalchemy.exc.InterfaceError, ConnectionError) as conn_err:
            logging.error(f"Database connection error: {conn_err}")
            raise ConnectionError from conn_err

        except sqlalchemy.exc.SQLAlchemyError as db_err:
            logging.error(f"Database error: {db_err}")
            await self._session.rollback()
            raise db_err

        except socket.gaierror as dns_err:
            logging.error(f"DNS resolution error: {dns_err}")
            raise ConnectionError

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            await self._session.rollback()
            raise e


class SaveDriverInfoUseCase:
    _repository: Type[ABCDriversRepository] = DriversRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    async def execute(self, driver_info: DriverInfo) -> int:
        try:
            async with self._session.begin():
                repository = self._repository(session=self._session)
                record_id = await repository.create(driver_info)
                await self._session.commit()
                logging.info(f"Driver data id={driver_info.driver_id} successfully saved {record_id=}")  # noqa E501
                return record_id

        except (sqlalchemy.exc.InterfaceError, ConnectionError) as conn_err:
            logging.error(f"Database connection error: {conn_err}")
            raise ConnectionError from conn_err

        except socket.gaierror as dns_err:
            logging.error(f"DNS resolution error: {dns_err}")
            raise ConnectionError

        except sqlalchemy.exc.SQLAlchemyError as db_err:
            logging.error(f"Database error: {db_err}")
            await self._session.rollback()
            raise db_err

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            await self._session.rollback()
            raise e


class GetUniqueDriversUseCase:

    _repository: Type[ABCDriversRepository] = DriversRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    async def execute(self) -> int:
        try:
            async with self._session.begin():
                repository = self._repository(session=self._session)

                await self._session.flush()
                return await repository.get_unique_driver_ids()

        except (sqlalchemy.exc.InterfaceError, ConnectionError, ) as conn_err:
            logging.error(f"Database connection error: {conn_err}")
            raise ConnectionError from conn_err

        except socket.gaierror as dns_err:
            logging.error(f"DNS resolution error: {dns_err}")
            raise ConnectionError

        except sqlalchemy.exc.SQLAlchemyError as db_err:
            logging.error(f"Database error: {db_err}")
            await self._session.rollback()
            raise db_err

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            await self._session.rollback()
            raise e
