from fastapi import APIRouter, HTTPException
from redis.asyncio import Redis

from app.core.config import settings

health_router = APIRouter()


@health_router.get("/live")
async def live():
    return {"status": "OK"}


@health_router.get("/ready")
async def ready():
    client = Redis.from_url(settings.redis_url, socket_connect_timeout=3, socket_timeout=3)
    try:
        await client.ping()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Outfit history is unavailable") from exc
    finally:
        await client.aclose()
    return {"status": "ok"}
