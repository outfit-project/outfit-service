from fastapi import FastAPI

from app.core.cors import setup_cors
from app.routers.health import health_router
from app.routers.outfit import outfit_router

app = FastAPI()

setup_cors(app)

app.include_router(health_router, prefix="/health")
app.include_router(outfit_router, prefix="/outfits")