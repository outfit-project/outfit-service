import random
from itertools import product
from app.schemas.items import ItemResponse

CATEGORY_GROUPS = {
    "top":       ["top", "shirt", "t-shirt", "blouse", "tank"],
    "outer":     ["outer", "outerwear", "jacket", "coat", "hoodie", "cardigan", "blazer", "sweater"],
    "bottom":    ["bottom", "pants", "jeans", "skirt", "shorts"],
    "shoes":     ["shoes", "sneakers", "boots", "sandals"],
    "accessory": ["accessory", "bag", "hat", "scarf"],
}


class ItemGrouper:
    def group(self, items: list[ItemResponse]) -> dict[str, list[ItemResponse]]:
        grouped: dict[str, list[ItemResponse]] = {}
        for item in items:
            if item.processing_status != "ready" or not item.embedding or not item.category:
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

    def outfit_combinations(
        self, grouped: dict[str, list[ItemResponse]]
    ) -> list[list[ItemResponse]]:
        base_tops = grouped.get("top", [])
        outers    = grouped.get("outer", [])
        bottoms   = grouped.get("bottom", [])
        shoes     = grouped.get("shoes", [])

        if not base_tops or not bottoms or not shoes:
            return []

        groups = [base_tops, bottoms, shoes, [None, *outers], [None, *grouped.get("accessory", [])]]
        total = 1
        for group in groups:
            total *= len(group)
        indices = range(total) if total <= 500 else random.sample(range(total), 500)
        combos = []
        for index in indices:
            combo = []
            for group in reversed(groups):
                index, offset = divmod(index, len(group))
                if group[offset] is not None:
                    combo.append(group[offset])
            combos.append(list(reversed(combo)))
        return combos

    def _resolve_group(self, category: str) -> str | None:
        c = category.lower()
        for group, values in CATEGORY_GROUPS.items():
            if c == group or c in values:
                return group
        return None
