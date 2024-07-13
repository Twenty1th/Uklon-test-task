from abc import ABC, abstractmethod

from domain.entities import DriverInfo


class ABCDriversRepository(ABC):

    @abstractmethod
    async def get(self, driver_id: int) -> DriverInfo: ...

    @abstractmethod
    async def create(self, driver_info: DriverInfo) -> int: ...
