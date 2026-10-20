from fastapi import APIRouter

from app.config import settings
from app.ml.embedder import get_embedder

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "version": settings.version,
        "embedder": get_embedder().name,
    }
