import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "Budgey API"
    version: str = "0.1.0"
    max_upload_bytes: int = int(os.getenv("BUDGEY_MAX_UPLOAD_BYTES", 5 * 1024 * 1024))
    match_threshold: float = float(os.getenv("BUDGEY_MATCH_THRESHOLD", 0.85))
    allowed_origins: tuple = tuple(
        o for o in os.getenv("BUDGEY_ALLOWED_ORIGINS", "*").split(",") if o
    )


settings = Settings()
