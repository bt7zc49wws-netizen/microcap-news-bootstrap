from fastapi.testclient import TestClient

from app.main import app


def test_status_endpoint_returns_freshness_contract() -> None:
    response = TestClient(app).get("/api/v1/status")

    assert response.status_code == 200
    body = response.json()
    data = body["data"]

    assert data["overall_status"] in {"ok", "degraded"}
    assert isinstance(data["is_stale"], bool)
    assert isinstance(data["freshness_threshold_seconds"], int)
    assert data["dependencies"]["read_model"] in {"ok", "unavailable"}
