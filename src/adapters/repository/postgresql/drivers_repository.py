import logging
from typing import Optional

from sqlalchemy import insert, select, distinct, func
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import DriverInfo, DriverPos
from domain.repository.repository import ABCDriversRepository
from domain.repository.models import DriverInfo as DriverInfoModel


class DriversRepository(ABCDriversRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, driver_info: DriverInfo) -> int:
        """Save driver info and return recordID

        :param driver_info: driver info
        :return: inserted record id
        """
        stmt = (insert(DriverInfoModel)
                .values(
            driver_id=driver_info.driver_id,
            driver_speed=driver_info.driver_speed,
            latitude=driver_info.driver_pos.latitude,
            longitude=driver_info.driver_pos.longitude,
            altitude=driver_info.driver_pos.altitude,
            created_at=driver_info.created_at,
            is_correct=driver_info.is_correct
        ).returning(DriverInfoModel.record_id))
        res = await self._session.execute(stmt)
        return res.scalar()

    async def get(self, driver_id: int) -> Optional[DriverInfo]:
        stmt = select(DriverInfoModel).where(
            DriverInfoModel.driver_id == driver_id
        ).order_by(DriverInfoModel.created_at.desc())
        res = (await self._session.execute(stmt)).scalar()
        if res:
            driver_pos = DriverPos(
                latitude=res.latitude,
                longitude=res.longitude,
                altitude=res.altitude,
            )
            return DriverInfo(
                driver_id=res.driver_id,
                driver_pos=driver_pos,
                driver_speed=res.driver_speed,
                created_at=res.created_at,
                is_correct=res.is_correct,
            )

    async def get_unique_driver_ids(self) -> list[DriverInfo]:
        stmt = select(func. count(DriverInfoModel.driver_id. distinct()))
        res = await self._session.execute(stmt)
        return res.scalar()
