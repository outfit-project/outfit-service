from app.interfaces.wardrobe_abc import IItemRepository


class OutfitService:
    def __init__(
            self,
            items: IItemRepository,
            grouper:
    ):
        self._items = items

