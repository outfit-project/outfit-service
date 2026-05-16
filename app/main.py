from fastapi import FastAPI

from app.routers.health import health_router
from app.routers.outfit import outfit_router

app = FastAPI()

app.include_router(health_router, prefix="/health")
app.include_router(outfit_router, prefix="/outfits")