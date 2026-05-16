from fastapi import FastAPI

from app.routers.health import health_router

app = FastAPI()

app.include_router(health_router, prefix="/health")
