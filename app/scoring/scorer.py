import numpy as np


class CosineSimilarityScorer:
    def score(self, a: list[float], b: list[float]) -> float:
        va = np.array(a)
        vb = np.array(b)

        norm = np.linalg.norm(va) * np.linalg.norm(vb)

        if norm == 0:
            return 0.0

        return float(np.dot(va, vb) / norm)