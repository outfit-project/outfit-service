from itertools import combinations
from app.schemas.items import ItemResponse
from app.scoring.scorer import CosineSimilarityScorer


class OutfitRanker:
    def __init__(self, scorer: CosineSimilarityScorer):
        self._scorer = scorer

    def rank(self, combos: list[list[ItemResponse]]) -> list[dict]:
        scored = []
        for combo in combos:
            score = self._score_combo(combo)
            scored.append({"score": score, "items": combo})
        return sorted(scored, key=lambda x: x["score"], reverse=True)

    def _score_combo(self, items: list[ItemResponse]) -> float:
        pairs = list(combinations(items, 2))
        if not pairs:
            return 0.0
        scores = [
            (self._scorer.score(a.embedding, b.embedding) + 1.0) / 2.0
            for a, b in pairs
            if a.embedding and b.embedding
        ]
        return sum(scores) / len(scores) if scores else 0.0
