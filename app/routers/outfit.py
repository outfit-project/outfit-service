from fastapi import APIRouter, Depends, Query

from app.core.security.deps import get_current_user, oauth2_scheme
from app.schemas.user import UserPayload
from app.use_cases.items import OutfitServiceDep

outfit_router = APIRouter()


@outfit_router.get("/suggest")
async def suggest(
    service: OutfitServiceDep,
    top_n: int = Query(default=5, ge=1, le=20),
    token: str = Depends(oauth2_scheme),
    current_user: UserPayload = Depends(get_current_user),
):
    return await service.get_outfit(token, top_n)