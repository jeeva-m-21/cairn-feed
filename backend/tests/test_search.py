from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_search_returns_matching_events_and_reasons() -> None:
    response = client.get("/v1/search", params={"q": "agent"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["query"] == "agent"
    assert len(payload["items"]) >= 1
    assert any("agent" in item["title"].lower() for item in payload["items"])
    assert all("matchReason" in item for item in payload["items"])


def test_search_requires_non_blank_query() -> None:
    response = client.get("/v1/search", params={"q": "   "})

    assert response.status_code == 422
