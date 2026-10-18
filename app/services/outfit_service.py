from app.interfaces.wardrobe_abc import IItemRepository
from app.interfaces.scoring_abc import IGrouper, IRanker, IOutfitCounter
from app.schemas.items import ItemListResponse


class OutfitService:
    def __init__(
            self,
            items: IItemRepository,
            grouper: IGrouper,
            ranker: IRanker,
            counter: IOutfitCounter,
    ):
        self._items = items
        self._grouper = grouper
        self._ranker = ranker
        self._counter = counter

    async def get_outfit(self, token: str, top_n: int = 5) -> dict:
        raw = await self._items.get_items(token)
        parsed = ItemListResponse(**raw)

        grouped = self._grouper.group(parsed.items)
        combos = self._grouper.outfit_combinations(grouped)

        if not combos:
            return {
                "items": [], "score": None,
                "message": "Add a top, a bottom and shoes, then wait until their photos are processed.",
            }

        ranked = self._ranker.rank(combos)[:max(1, top_n)]
        adjusted = await self._apply_counter(ranked)

        if not adjusted:
            return {"items": [], "score": None, "message": "No compatible outfit is available yet."}

        best = adjusted[0]
        await self._increment_shown([best])

        return {"items": best["items"], "score": best["score"], "message": None}

    async def _apply_counter(self, ranked: list[dict]) -> list[dict]:
        for entry in ranked:
            key = self._build_key(entry["items"])
            shown = await self._counter.get(key)
            entry["adjusted_score"] = entry["score"] / (1 + shown)
        return sorted(ranked, key=lambda x: x["adjusted_score"], reverse=True)

    async def _increment_shown(self, outfits: list[dict]) -> None:
        for entry in outfits:
            key = self._build_key(entry["items"])
            await self._counter.increment(key)

    def _build_key(self, items) -> str:
        ids = sorted(str(item.id) for item in items)
        return "outfit_shown:" + ":".join(ids)
