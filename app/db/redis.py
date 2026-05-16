from redis.asyncio import Redis
from app.interfaces.scoring_abc import IOutfitCounter


class RedisDB(IOutfitCounter):
    def __init__(self, redis_url: str):
        self._client = Redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> int:
        value = await self._client.get(key)
        return int(value) if value else 0

    async def increment(self, key: str, ttl: int = 604800) -> None:
        await self._client.incr(key)
        await self._client.expire(key, ttl)

    async def close(self) -> None:
        await self._client.aclose()