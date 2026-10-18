import math

CATEGORY_GROUPS = {
    "top": ["top", "shirt", "t-shirt", "blouse", "tank"],
    "outer": ["outer", "jacket", "coat", "hoodie", "cardigan", "blazer", "sweater"],
    "bottom": ["bottom", "pants", "jeans", "skirt", "shorts"],
    "shoes": ["shoes", "sneakers", "boots", "sandals"],
    "accessory": ["accessory", "bag", "hat", "scarf"],
}

COMPATIBLE_PAIRS = {
    ("base_top", "bottom"),
    ("base_top", "shoes"),
    ("bottom", "shoes"),
    ("outer", "base_top"),
    ("outer", "bottom"),
    ("outer", "shoes"),
    ("base_top", "outer"),
    ("outer", "top"),
}


class CosineSimilarityScorer:
    def score(self, a: list[float], b: list[float]) -> float:
        if not a or len(a) != len(b) or not all(math.isfinite(x) for x in (*a, *b)):
            return 0.0
        norm_a, norm_b = math.hypot(*a), math.hypot(*b)
        if not norm_a or not norm_b:
            return 0.0
        score = sum((x / norm_a) * (y / norm_b) for x, y in zip(a, b))
        return max(-1.0, min(1.0, score))
