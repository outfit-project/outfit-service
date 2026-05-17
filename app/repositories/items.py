import httpx
from fastapi import HTTPException, status


class ItemRepository:
    def __init__(self, api_url: str, timeout: float = 30.0):
        self._api = api_url
        self._timeout = timeout

    async def get_items(self, token: str):
        if not self._api:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ITEMS_URL is not configured",
            )
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(
                    self._api,
                    headers={"Authorization": f"Bearer {token}"},
                )
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    f"Cannot reach wardrobe at {self._api}. "
                    "In Docker use http://wardrobe-service:8000/items/ "
                    "and attach outfit-service to the wardrobe network."
                ),
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.text,
            ) from exc
