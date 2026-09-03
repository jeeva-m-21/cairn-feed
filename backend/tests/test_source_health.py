from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_source_health_reports_permitted_source_statuses() -> None:
    response = client.get("/v1/admin/source-health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["overallStatus"] == "healthy"
    assert {source["sourceId"] for source in payload["sources"]} >= {"rss", "github", "arxiv"}
    assert all(source["status"] in {"healthy", "degraded", "disabled"} for source in payload["sources"])
    assert all("lastCheckedAt" in source for source in payload["sources"])


def test_source_health_can_mark_a_source_degraded() -> None:
    response = client.get("/v1/admin/source-health?degraded=github")

    assert response.status_code == 200
    payload = response.json()
    github = next(source for source in payload["sources"] if source["sourceId"] == "github")
    assert payload["overallStatus"] == "degraded"
    assert github["status"] == "degraded"
