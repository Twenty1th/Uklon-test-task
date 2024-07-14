from abc import ABC, abstractmethod
from typing import List

from domain.entities import DriverInfo


class ABCDriversRepository(ABC):

    @abstractmethod
    async def get(self, driver_id: int) -> DriverInfo: ...

    @abstractmethod
    async def create(self, driver_info: DriverInfo) -> int: ...

    @abstractmethod
    async def get_unique_driver_ids(self) -> List[int]: ...
