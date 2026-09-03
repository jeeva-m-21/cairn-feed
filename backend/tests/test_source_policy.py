from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_github_adapter_rejects_non_github_host() -> None:
    response = client.post("/v1/ingest/github", params={"url": "https://example.com/release"})

    assert response.status_code == 422
    assert response.json()["detail"] == "URL host is not permitted for this adapter"


def test_arxiv_adapter_rejects_non_arxiv_host() -> None:
    response = client.post("/v1/ingest/arxiv", params={"url": "https://example.com/paper"})

    assert response.status_code == 422
    assert response.json()["detail"] == "URL host is not permitted for this adapter"
