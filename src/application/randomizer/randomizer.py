import asyncio
import logging
import random
import sys

import httpx

from domain.entities import DriverInfo, DriverPos
from settings import CONFIG
from logger import setup_logger

setup_logger()


class Randomizer:

    def generate_random_driver_info(self):
        return DriverInfo(
            driver_id=self.generate_random_id(),
            driver_pos=self.generate_random_pos(),
            driver_speed=self.generate_speed()
        )

    def generate_random_pos(self) -> DriverPos:
        random_longitude_offset = random.uniform(
            -CONFIG.randomizer.longitude_range,
            CONFIG.randomizer.longitude_range
        )
        random_latitude_offset = random.uniform(
            -CONFIG.randomizer.latitude_range,
            CONFIG.randomizer.latitude_range
        )
        random_altitude_offset = random.uniform(
            -CONFIG.randomizer.altitude_range,
            CONFIG.randomizer.altitude_range
        )
        return DriverPos(
            longitude=round(CONFIG.randomizer.latitude_start + random_longitude_offset, 4),
            latitude=round(CONFIG.randomizer.latitude_start + random_latitude_offset, 4),
            altitude=round(CONFIG.randomizer.altitude_start + random_altitude_offset, 2),
        )

    def generate_speed(self) -> int:
        return random.randint(0, CONFIG.randomizer.speed_limit)

    def generate_random_id(self) -> int:
        return random.randint(0, CONFIG.randomizer.drivers_count)


async def send_data(driver_info: DriverInfo) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(CONFIG.randomizer.api_addr, json=driver_info.model_dump())


