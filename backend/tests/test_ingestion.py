from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_ingest_rss_returns_normalized_document() -> None:
    rss_url = "https://example.com/fixture.rss"  # fixture-safe RSS
    response = client.post("/v1/ingest/rss", params={"url": rss_url})

    assert response.status_code == 201
    payload = response.json()
    assert "documentId" in payload
    assert payload["sourceUrl"] == rss_url
    assert "title" in payload
    assert "publishedAt" in payload
    assert "excerpt" in payload
    assert len(payload["entities"]) >= 1
