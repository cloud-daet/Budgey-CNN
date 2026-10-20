import numpy as np
from fastapi import APIRouter, HTTPException

from app.config import settings
from app.ml.similarity import top_k_cosine
from app.schemas import Match, MatchRequest, MatchResponse

router = APIRouter(prefix="/v1", tags=["cnn"])


@router.post("/match", response_model=MatchResponse)
def match(req: MatchRequest):
    """Stateless similarity search: the app sends its stored embeddings,
    the server returns the closest ones. Optional; the same search can run
    on-device if preferred."""
    threshold = req.threshold if req.threshold is not None else settings.match_threshold
    if not req.candidates:
        return MatchResponse(matched=False, matches=[], threshold=threshold)

    dim = len(req.embedding)
    if any(len(c.embedding) != dim for c in req.candidates):
        raise HTTPException(422, "All embeddings must have the same length")

    matrix = np.asarray([c.embedding for c in req.candidates], dtype=np.float32)
    ranked = top_k_cosine(np.asarray(req.embedding, dtype=np.float32), matrix, req.top_k)
    matches = [Match(id=req.candidates[i].id, score=s) for i, s in ranked]
    return MatchResponse(
        matched=bool(matches and matches[0].score >= threshold),
        matches=matches,
        threshold=threshold,
    )
