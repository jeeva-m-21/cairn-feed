from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_ingest_github_release_normalizes_document() -> None:
    response = client.post(
        "/v1/ingest/github",
        params={"url": "https://github.com/cairn-fixture/repo/releases/tag/v1.0.0"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["sourceUrl"].startswith("https://github.com/")
    assert payload["title"] == "Cairn Fixture v1.0.0"
    assert payload["entities"] == ["cairn-fixture", "repo"]


def test_ingest_arxiv_normalizes_document() -> None:
    response = client.post(
        "/v1/ingest/arxiv",
        params={"url": "https://arxiv.org/abs/2401.00001"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["sourceUrl"] == "https://arxiv.org/abs/2401.00001"
    assert payload["title"] == "Cairn Fixture Research Paper"
    assert "reasoning" in payload["entities"]
