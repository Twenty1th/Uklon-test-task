from __future__ import annotations

from pathlib import Path
from typing import Optional

import ujson
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    speed_limit: float = float("-inf")
    altitude_limit: float = float("-inf")

    @classmethod
    def from_json(cls, path: Path) -> Settings:
        with open(path, "r") as f:
            settings = ujson.load(f)
            return cls(
                latitude_limit=settings["latitude_limit"],
                longitude_limit=settings["longitude_limit"],
                speed_limit=settings["speed_limit"],
                altitude=settings["altitude_limit"],
            )


CONFIG: Optional[Settings] = None


def load_settings() -> None:
    global CONFIG
    CONFIG = Settings.from_json(Path(__file__).parent / "settings.json")
