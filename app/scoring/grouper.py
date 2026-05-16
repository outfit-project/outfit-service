from itertools import product
from app.schemas.items import ItemResponse

CATEGORY_GROUPS = {
    "top":       ["top", "shirt", "jacket", "hoodie", "sweater"],
    "bottom":    ["bottom", "pants", "jeans", "skirt", "shorts"],
    "shoes":     ["shoes", "sneakers", "boots", "sandals"],
    "accessory": ["accessory", "bag", "hat", "scarf"],
}


class ItemGrouper:
    def group(self, items: list[ItemResponse]) -> dict[str, list[ItemResponse]]:
        grouped: dict[str, list[ItemResponse]] = {}
        for item in items:
            if not item.embedding:
                continue
            group = self._resolve_group(item.category)
            if group:
                grouped.setdefault(group, []).append(item)
        return grouped

    def combinations(self, grouped: dict[str, list[ItemResponse]]) -> list[list[ItemResponse]]:
        tops      = grouped.get("top", [])
        bottoms   = grouped.get("bottom", [])
        shoes     = grouped.get("shoes", [])
        accessory = grouped.get("accessory", [])

        if not tops or not bottoms:
            return []

        base = list(product(tops, bottoms))
        with_shoes = [list(b) + [s] for b, s in product(base, shoes)] if shoes else [list(b) for b in base]
        if accessory:
            return [c + [a] for c, a in product(with_shoes, accessory)]
        return with_shoes

    def _resolve_group(self, category: str) -> str | None:
        c = category.lower()
        for group, values in CATEGORY_GROUPS.items():
            if c == group or c in values:
                return group
        return None