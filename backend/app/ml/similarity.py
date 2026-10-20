import numpy as np


def top_k_cosine(query: np.ndarray, matrix: np.ndarray, k: int) -> list[tuple[int, float]]:
    """Return (row_index, cosine_score) for the k best rows, best first."""
    q = query / (np.linalg.norm(query) or 1.0)
    norms = np.linalg.norm(matrix, axis=1)
    norms[norms == 0] = 1.0
    scores = (matrix / norms[:, None]) @ q
    order = np.argsort(-scores)[:k]
    return [(int(i), float(scores[i])) for i in order]
