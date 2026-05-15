import httpx


class ItemRepository:
    def __init__(
            self,
            api_url: str
    ):
        self._api = api_url

    async def get_items(self, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._api,
                headers={'Authorization': f'Bearer {token}'}
            )
            response.raise_for_status()
            return response.json()
