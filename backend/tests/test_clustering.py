from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_cluster_groups_related_documents_into_one_event() -> None:
    response = client.post(
        "/v1/clusters",
        json={
            "documents": [
                {
                    "documentId": "doc-a",
                    "sourceUrl": "https://example.com/a",
                    "title": "Compact reasoning models reach edge devices",
                    "excerpt": "Small models improve local inference.",
                    "entities": ["reasoning", "inference", "edge"],
                },
                {
                    "documentId": "doc-b",
                    "sourceUrl": "https://example.com/b",
                    "title": "New efficient inference models run locally",
                    "excerpt": "Edge deployments become more practical.",
                    "entities": ["reasoning", "inference", "edge"],
                },
            ]
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert len(payload["clusters"]) == 1
    cluster = payload["clusters"][0]
    assert cluster["documentIds"] == ["doc-a", "doc-b"]
    assert cluster["confidence"] == "high"
    assert "shared entities" in cluster["explanation"].lower()


def test_cluster_is_idempotent_for_same_documents() -> None:
    request = {
        "documents": [
            {
                "documentId": "doc-same",
                "sourceUrl": "https://example.com/same",
                "title": "Agent tooling update",
                "excerpt": "Durable primitives for agents.",
                "entities": ["agents", "tooling"],
            }
        ]
    }

    first = client.post("/v1/clusters", json=request)
    second = client.post("/v1/clusters", json=request)

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json() == second.json()
