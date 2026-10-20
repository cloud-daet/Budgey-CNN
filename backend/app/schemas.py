from pydantic import BaseModel, Field


class EmbedResponse(BaseModel):
    embedding: list[float]
    dim: int
    model: str


class Candidate(BaseModel):
    id: str
    embedding: list[float]


class MatchRequest(BaseModel):
    embedding: list[float]
    candidates: list[Candidate] = Field(max_length=5000)
    top_k: int = Field(default=3, ge=1, le=20)
    threshold: float | None = Field(default=None, ge=-1.0, le=1.0)


class Match(BaseModel):
    id: str
    score: float


class MatchResponse(BaseModel):
    matched: bool
    matches: list[Match]
    threshold: float
