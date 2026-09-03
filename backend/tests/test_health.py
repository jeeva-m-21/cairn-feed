from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_health_reports_service_readiness() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "cairn-api"}
