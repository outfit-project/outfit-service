import os
from dataclasses import dataclass

@dataclass
class Config:
    items_url: str = os.getenv("ITEMS_URL", "")
    redis_url: str = os.getenv("REDIS_URL", "")
    secret_key: str = os.getenv("SECRET_KEY", "")
    algorithm: str = "HS256"


settings = Config()