import os
from dataclasses import dataclass


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    return int(raw)


@dataclass
class Config:
    items_url: str = os.getenv("ITEMS_URL", "")
    cors_origins: str = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    )
    redis_url: str = os.getenv("REDIS_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_EXPIRE_MIN: int = _int_env("ACCESS_EXPIRE_MIN", 15)
    REFRESH_EXPIRE_DAYS: int = _int_env("REFRESH_EXPIRE_DAYS", 30)


settings = Config()