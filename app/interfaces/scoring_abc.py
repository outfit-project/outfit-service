from typing import Protocol, runtime_checkable

from app.schemas.items import ItemResponse


@runtime_checkable
class IGrouper(Protocol):
    def group(self, items: list[ItemResponse]) -> dict[str, list[ItemResponse]]:
        pass

    def combinations(self, grouped: dict[str, list[ItemResponse]]) -> list[list[ItemResponse]]:
        pass


@runtime_checkable
class IRanker(Protocol):
    def rank(self, combos: list[list[ItemResponse]]) -> list[dict]:
        pass


@runtime_checkable
class IOutfitCounter(Protocol):
    async def get(self, key: str) -> int:
        pass

    async def increment(self, key: str) -> None:
        pass
