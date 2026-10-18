from typing import Annotated
from collections.abc import AsyncIterator
from fastapi import Depends
from app.core.config import settings
from app.db.redis import RedisDB
from app.repositories.items import ItemRepository
from app.scoring.grouper import ItemGrouper
from app.scoring.ranker import OutfitRanker
from app.scoring.scorer import CosineSimilarityScorer
from app.services.outfit_service import OutfitService


async def get_outfit_service_case() -> AsyncIterator[OutfitService]:
    counter = RedisDB(settings.redis_url)
    try:
        yield OutfitService(
            items=ItemRepository(settings.items_url),
            grouper=ItemGrouper(),
            ranker=OutfitRanker(CosineSimilarityScorer()),
            counter=counter,
        )
    finally:
        await counter.close()


OutfitServiceDep = Annotated[
    OutfitService,
    Depends(get_outfit_service_case),
]
