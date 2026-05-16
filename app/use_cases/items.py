from typing import Annotated
from fastapi import Depends
from app.core.config import settings
from app.db.redis import RedisDB
from app.repositories.items import ItemRepository
from app.scoring.grouper import ItemGrouper
from app.scoring.ranker import OutfitRanker
from app.scoring.scorer import CosineSimilarityScorer
from app.services.outfit_service import OutfitService


def get_outfit_service_case() -> OutfitService:
    return OutfitService(
        items=ItemRepository(settings.items_url),
        grouper=ItemGrouper(),
        ranker=OutfitRanker(CosineSimilarityScorer()),
        counter=RedisDB(settings.redis_url),
    )


OutfitServiceDep = Annotated[
    OutfitService,
    Depends(get_outfit_service_case),
]