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


def test_health_allows_the_configured_dashboard_origin() -> None:
    response = TestClient(app).options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
