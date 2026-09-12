from fastapi import FastAPI


app = FastAPI(title="ThreatSentry API", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, object]:
    """Return the non-sensitive service readiness state."""
    return {
        "status": "ok",
        "service": "threatsentry-api",
        "model": {"status": "not_ready", "version": None},
    }
