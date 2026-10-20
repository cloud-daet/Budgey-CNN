"""Image -> embedding.

The real CNN (pre-trained feature extractor, TFLite or PyTorch) is still being
decided. Anything that implements `Embedder` can be swapped in via
`get_embedder()` without touching the routers.
"""
from functools import lru_cache
from typing import Protocol

import numpy as np
from PIL import Image


class Embedder(Protocol):
    name: str
    dim: int

    def embed(self, image: Image.Image) -> np.ndarray:
        """Return an L2-normalised float32 vector of length `dim`."""
        ...


class PlaceholderEmbedder:
    """Grid-average colour features. Only for wiring/testing the pipeline;
    NOT a product-recognition model."""

    name = "placeholder-color-grid"
    grid = 4
    dim = grid * grid * 3

    def embed(self, image: Image.Image) -> np.ndarray:
        img = image.convert("RGB").resize((64, 64))
        arr = np.asarray(img, dtype=np.float32) / 255.0
        cell = 64 // self.grid
        feats = arr.reshape(self.grid, cell, self.grid, cell, 3).mean(axis=(1, 3))
        vec = feats.reshape(-1)
        vec = vec - vec.mean()
        norm = np.linalg.norm(vec)
        return (vec / norm if norm > 0 else vec).astype(np.float32)


@lru_cache(maxsize=1)
def get_embedder() -> Embedder:
    # TODO: load the trained CNN here (TFLite interpreter or torch model)
    return PlaceholderEmbedder()
