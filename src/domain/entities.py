from __future__ import annotations

import logging
import time

from pydantic import BaseModel, Field

from domain.distance_calculator import DistanceCalculator
import settings

type DriverId = int


class DriverInfo(BaseModel):
    driver_id: DriverId
    driver_pos: DriverPos
    driver_speed: int
    created_at: int = Field(
        alias="created_at",
        default_factory=lambda: int(time.time()),
    )
    is_correct: bool = Field(
        default=False,
    )

    def is_valid(self) -> bool:
        if any([
            settings.CONFIG.speed_limit < self.driver_speed,
            self.driver_speed < 0,
            self.driver_pos.altitude < 0,
            settings.CONFIG.longitude_limit < self.driver_pos.longitude,
        ]):
            logging.info(f"Incorrect driver data {self}")
            return False

        return True

    def is_valid_distance(self, last_pos: DriverInfo) -> bool:
        calculator = DistanceCalculator(
            driver_last_pos=last_pos.driver_pos,
            driver_cur_pos=self.driver_pos,
            time_elapsed=(self.created_at - last_pos.created_at) / 3600.0
        )
        distance = calculator.calculate_3d_distance()
        average_speed = calculator.calculate_average_speed(distance)
        logging.debug(f'[Driver {self.driver_id}] average speed : {average_speed:.2f} км/ч"')  # noqa: E501
        if settings.CONFIG.speed_limit < average_speed:
            logging.info(
                f"Incorrect driver speed {average_speed} > {settings.CONFIG.speed_limit}")  # noqa: E501
            return False
        return True


class DriverPos(BaseModel):
    latitude: float
    longitude: float
    altitude: float
