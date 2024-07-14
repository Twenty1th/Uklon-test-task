from __future__ import annotations

from pathlib import Path
from typing import Optional, Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

type AppType = Literal['api', 'randomizer']

CONFIG_PATH = Path(__file__).parent / "settings.json"


class APISettings(BaseModel):
    latitude_limit: float = float("-inf")
    longitude_limit: float = float("-inf")
    altitude_limit: float = float("-inf")
    speed_limit: float = float("-inf")
    postgres_url: PostgresDsn = "postgresql+asyncpg://postgres:password@127.0.0.1:5433"
    postgres_echo: bool = False
    postgres_pool_size: int = 5


class RandomizerSettings(BaseModel):
    drivers_count: int = 100
    latitude_start: float = float("-inf")
    longitude_start: float = float("-inf")
    altitude_start: float = float("-inf")
    latitude_range: float = float("-inf")
    longitude_range: float = float("-inf")
    altitude_range: float = float("-inf")


class Settings(BaseSettings):

    api: APISettings = APISettings()
    randomizer: RandomizerSettings = RandomizerSettings()


CONFIG: Optional[APISettings | RandomizerSettings] = None


def load_settings(app_name: AppType) -> None:
    global CONFIG
    settings = Settings.parse_file(CONFIG_PATH)
    match app_name:
        case "api":
            CONFIG = settings.api
        case "randomizer":
            CONFIG = settings.randomizer
        case _:
            raise ValueError(f"Unavailable app name {app_name}")
