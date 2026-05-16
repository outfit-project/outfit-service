from typing import runtime_checkable, Protocol


@runtime_checkable
class IItemRepository(Protocol):
    async def  get_items(self, token: str):
        pass