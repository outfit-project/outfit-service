from typing import Protocol, runtime_checkable

from app.schemas.items import ItemResponse


@runtime_checkable
class IGrouper(Protocol):
    def group(self, items: list[ItemResponse]) -> dict[str, list[ItemResponse]]:
        pass

