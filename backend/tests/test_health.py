from fastapi.testclient import TestClient

from backend.main import app


def test_health_reports_api_and_model_readiness() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "threatsentry-api",
        "model": {"status": "not_ready", "version": None},
    }
