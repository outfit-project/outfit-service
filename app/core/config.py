import os


class Config:
    items_url: str = os.getenv("ITEMS_URL")

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_EXPIRE_MIN: int = 15
    REFRESH_EXPIRE_DAYS: int = 30

settings = Config()