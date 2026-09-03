from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_cluster_rejects_duplicate_document_ids() -> None:
    response = client.post(
        "/v1/clusters",
        json={
            "documents": [
                {
                    "documentId": "doc-duplicate",
                    "sourceUrl": "https://example.com/one",
                    "title": "First report",
                    "excerpt": "First excerpt.",
                    "entities": ["agents"],
                },
                {
                    "documentId": "doc-duplicate",
                    "sourceUrl": "https://example.com/two",
                    "title": "Second report",
                    "excerpt": "Second excerpt.",
                    "entities": ["agents"],
                },
            ]
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Duplicate document IDs are not allowed"
