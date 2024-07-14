from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

__all__ = ["CONFIG", "load_settings"]

CONFIG_PATH = Path(__file__).parent / "settings.json"


class PgSQLSettings(BaseSettings):
    postgres_url: PostgresDsn | str = "postgresql+asyncpg://postgres:password@127.0.0.1:5433"
    postgres_echo: bool = False
    postgres_pool_size: int = 5


class APISettings(BaseModel):
    port: int = 8000
    altitude_limit: float = float("-inf")
    speed_limit: float = float("-inf")


class RandomizerSettings(BaseModel):
    drivers_count: int = 100
    speed_limit: int = 200
    latitude_start: float = float("-inf")
    longitude_start: float = float("-inf")
    altitude_start: float = float("-inf")
    latitude_range: float = float("-inf")
    longitude_range: float = float("-inf")
    altitude_range: float = float("-inf")
    api_addr: str = "http://localhost:8000/api/v1/driver-geo"
    requests_delay: int = 1


class Settings(BaseSettings):
    api: APISettings = APISettings()
    randomizer: RandomizerSettings = RandomizerSettings()
    pgsql: PgSQLSettings = PgSQLSettings()


CONFIG: Optional[Settings] = None


def load_settings() -> None:
    global CONFIG
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        CONFIG = Settings.model_validate(json.load(f))


load_settings()
