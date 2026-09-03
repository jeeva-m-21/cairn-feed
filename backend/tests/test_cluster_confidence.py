from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_cluster_keeps_unrelated_documents_separate_with_low_confidence() -> None:
    response = client.post(
        "/v1/clusters",
        json={
            "documents": [
                {
                    "documentId": "doc-model",
                    "sourceUrl": "https://example.com/model",
                    "title": "Open model release",
                    "excerpt": "A compact model for local inference.",
                    "entities": ["models", "inference"],
                },
                {
                    "documentId": "doc-security",
                    "sourceUrl": "https://example.com/security",
                    "title": "New developer security scanner",
                    "excerpt": "Static analysis finds supply chain risks.",
                    "entities": ["security", "static-analysis"],
                },
            ]
        },
    )

    assert response.status_code == 201
    clusters = response.json()["clusters"]
    assert len(clusters) == 2
    assert all(cluster["confidence"] == "low" for cluster in clusters)
    assert all("kept separate" in cluster["explanation"].lower() for cluster in clusters)
