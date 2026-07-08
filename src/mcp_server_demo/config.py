"""Configuración del servidor MCP (settings tipadas desde entorno/.env)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_path: str = Field(default="./data/demo.db", alias="DB_PATH")
    geocode_url: str = Field(
        default="https://geocoding-api.open-meteo.com/v1/search", alias="GEOCODE_URL"
    )
    forecast_url: str = Field(
        default="https://api.open-meteo.com/v1/forecast", alias="FORECAST_URL"
    )
    http_timeout: float = Field(default=10.0, alias="HTTP_TIMEOUT")

    def path(self, value: str) -> Path:
        p = Path(value)
        return p if p.is_absolute() else (ROOT_DIR / p)

    @property
    def db_file(self) -> Path:
        return self.path(self.db_path)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
