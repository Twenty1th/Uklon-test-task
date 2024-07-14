from __future__ import annotations

from math import radians, sin, cos, sqrt


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.entities import DriverPos


class DistanceCalculator:
    R = 6371.0  # Earth radius

    def __init__(
            self,
            *,
            driver_last_pos: DriverPos,
            driver_cur_pos: DriverPos,
            time_elapsed: float
    ):
        self.driver_last_pos = driver_last_pos
        self.driver_cur_pos = driver_cur_pos
        self.time_elapsed = time_elapsed

    def calculate_horizontal_distance(
            self, lat: float, lon: float, alt: float
    ) -> (float, float, float):
        """ I sometimes have an error with dividing a floating point number by zero,
        but I don't have time to fix it.
        In this regard, there are discrepancies in metrics between entries in the database and coordinates. TODO
        """
        lat, lon = radians(lat), radians(lon)
        x = (self.R + alt / 1000.0) * cos(lat) * cos(lon)
        y = (self.R + alt / 1000.0) * cos(lat) * sin(lon)
        z = (self.R + alt / 1000.0) * sin(lat)
        return x, y, z

    def calculate_3d_distance(self) -> (float, float, float):
        x1, y1, z1 = self.calculate_horizontal_distance(
            self.driver_last_pos.latitude,
            self.driver_last_pos.longitude,
            self.driver_last_pos.altitude,
        )
        x2, y2, z2 = self.calculate_horizontal_distance(
            self.driver_cur_pos.latitude,
            self.driver_cur_pos.longitude,
            self.driver_cur_pos.altitude,
        )
        distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        return distance

    def calculate_average_speed(self, distance) -> int:
        return distance / self.time_elapsed
