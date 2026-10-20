# Budgey backend

Stateless FastAPI service. No database, no accounts, no photo storage: photos and
embeddings live on the device. The server only runs the ML parts.

## Run

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0
```

Docs: http://localhost:8000/docs

## Test

```bash
pytest
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness + which embedder is loaded |
| POST | `/v1/embed` | Multipart `file` (compressed thumbnail) -> CNN embedding |
| POST | `/v1/match` | Embedding + the app's stored embeddings -> best matches (optional; can also be done on-device) |
| POST | `/v1/forecast` | ARIMA weekly forecast. Returns 501 until implemented |

Flow for a new photo: app sends thumbnail to `/embed`, then compares the embedding
to its stored ones (locally or via `/match`). On a match above the threshold it
autofills name and category; otherwise the user enters them and the app saves the
new embedding.

## Where to plug things in

- **CNN**: `app/ml/embedder.py`. `PlaceholderEmbedder` is a colour-grid stub for
  wiring only. Replace `get_embedder()` with the trained model (TFLite or PyTorch,
  still undecided); keep the `Embedder` interface.
- **ARIMA**: `app/routers/forecast.py` (postponed).
- **Settings**: env vars `BUDGEY_MAX_UPLOAD_BYTES`, `BUDGEY_MATCH_THRESHOLD`,
  `BUDGEY_ALLOWED_ORIGINS` (see `.env.example`).

## Layout

```
app/
  main.py          app + CORS + routers
  config.py        env-based settings
  schemas.py       request/response models
  routers/         health, embed, match, forecast
  ml/              embedder (swap point), similarity
tests/test_api.py
```
