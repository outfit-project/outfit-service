import numpy as np

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
        va = np.array(a)
        vb = np.array(b)

        norm = np.linalg.norm(va) * np.linalg.norm(vb)

        if norm == 0:
            return 0.0

        return float(np.dot(va, vb) / norm)