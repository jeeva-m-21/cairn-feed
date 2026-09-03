from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_brief_generates_claims_from_cluster_with_evidence() -> None:
    cluster_response = client.post(
        "/v1/clusters",
        json={
            "documents": [
                {
                    "documentId": "doc-model-a",
                    "sourceUrl": "https://example.com/a",
                    "title": "Compact reasoning models",
                    "excerpt": "Small models improve local inference on edge devices.",
                    "entities": ["reasoning", "inference", "edge"],
                },
                {
                    "documentId": "doc-model-b",
                    "sourceUrl": "https://example.com/b",
                    "title": "Efficient inference models for local run",
                    "excerpt": "Edge deployments practical with new models.",
                    "entities": ["reasoning", "inference", "edge"],
                },
            ]
        },
    )
    cluster_id = cluster_response.json()["clusters"][0]["clusterId"]

    brief_response = client.post("/v1/briefs", json={"clusterId": cluster_id})

    assert brief_response.status_code == 201
    payload = brief_response.json()
    assert "briefId" in payload
    assert len(payload["claims"]) >= 1
    claim = payload["claims"][0]
    assert "text" in claim
    assert "confidence" in claim
    assert len(claim["evidence"]) >= 1
    evidence = claim["evidence"][0]
    assert "documentId" in evidence
    assert "citation" in evidence