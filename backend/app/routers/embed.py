import io

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.config import settings
from app.ml.embedder import get_embedder
from app.schemas import EmbedResponse

router = APIRouter(prefix="/v1", tags=["cnn"])


@router.post("/embed", response_model=EmbedResponse)
def embed(file: UploadFile = File(...)):
    """Take the compressed in-app thumbnail, return its CNN embedding.
    Nothing is stored; the app keeps the embedding locally."""
    data = file.file.read(settings.max_upload_bytes + 1)
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(413, "Image too large")
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(415, "Unsupported or corrupt image")

    embedder = get_embedder()
    vec = embedder.embed(image)
    return EmbedResponse(embedding=vec.tolist(), dim=embedder.dim, model=embedder.name)
