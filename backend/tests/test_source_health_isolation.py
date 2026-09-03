from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_source_health_degradation_probe_does_not_mutate_next_health_check() -> None:
    client.get("/v1/admin/source-health?degraded=github")

    response = client.get("/v1/admin/source-health")

    assert response.status_code == 200
    assert response.json()["overallStatus"] == "healthy"
