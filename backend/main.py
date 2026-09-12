from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import get_settings


app = FastAPI(title="ThreatSentry API", version="0.1.0")
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-Id"],
)


@app.get("/health")
async def health() -> dict[str, object]:
    """Return the non-sensitive service readiness state."""
    return {
        "status": "ok",
        "service": "threatsentry-api",
        "model": {"status": "not_ready", "version": None},
    }
