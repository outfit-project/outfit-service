from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/live")
async def live():
    return {"status": "OK"}
