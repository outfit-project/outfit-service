import math
from uuid import uuid4

import pytest

from app.scoring.grouper import ItemGrouper
from app.scoring.ranker import OutfitRanker
from app.scoring.scorer import CosineSimilarityScorer
from app.schemas.items import ItemResponse
from app.services.outfit_service import OutfitService


def item(category, *, status="ready", embedding=None):
    return {
        "id": str(uuid4()), "user_id": str(USER_ID), "category": category,
        "image_url": "/items/example/image", "embedding": embedding or [1.0, 0.0],
        "processing_status": status, "subcategory": "test", "style": "casual",
        "color_hex": "#102030",
    }


USER_ID = uuid4()


class Inventory:
    def __init__(self, items):
        self.items = items

    async def get_items(self, token):
        return {"items": self.items, "total": len(self.items)}


class History:
    def __init__(self):
        self.values = {}

    async def get(self, key):
        return self.values.get(key, 0)

    async def increment(self, key):
        self.values[key] = self.values.get(key, 0) + 1


def service(items):
    return OutfitService(Inventory(items), ItemGrouper(), OutfitRanker(CosineSimilarityScorer()), History())


@pytest.mark.asyncio
async def test_ready_outfit_returns_real_score_and_metadata():
    result = await service([item("top"), item("bottom"), item("shoes")]).get_outfit("token")
    assert isinstance(result, dict)
    assert len(result["items"]) == 3
    assert result["score"] == pytest.approx(1.0)
    assert result["items"][0].color_hex == "#102030"
    assert result["message"] is None


@pytest.mark.asyncio
async def test_pending_and_failed_items_cannot_enter_an_outfit():
    result = await service([item("top", status="pending"), item("top", status="failed"), item("bottom"), item("shoes")]).get_outfit("token")
    assert result["items"] == []
    assert result["score"] is None
    assert result["message"]


@pytest.mark.asyncio
async def test_shown_history_rotates_equally_compatible_outfits():
    wardrobe = service([item("top"), item("top"), item("bottom"), item("shoes")])
    first = await wardrobe.get_outfit("token", top_n=2)
    second = await wardrobe.get_outfit("token", top_n=2)
    assert {i.id for i in first["items"]} != {i.id for i in second["items"]}


def test_outerwear_and_accessories_are_supported_without_exploding_combinations():
    grouped = ItemGrouper().group([ItemResponse(**item(c)) for c in ("top", "bottom", "shoes", "outerwear", "accessory")])
    combos = ItemGrouper().outfit_combinations(grouped)
    assert any(any(i.category == "outerwear" for i in combo) for combo in combos)
    assert any(any(i.category == "accessory" for i in combo) for combo in combos)
    assert len(combos) <= 500


@pytest.mark.parametrize("a,b", [([1, 2], [1]), ([float("nan")], [1]), ([float("inf")], [1]), ([], [])])
def test_malformed_embeddings_produce_a_finite_score(a, b):
    score = CosineSimilarityScorer().score(a, b)
    assert math.isfinite(score)
    assert -1 <= score <= 1


@pytest.mark.asyncio
async def test_empty_inventory_has_actionable_response():
    result = await service([]).get_outfit("token")
    assert result["items"] == []
    assert result["score"] is None
    assert "top" in result["message"].lower()
