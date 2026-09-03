import json

from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def _create_cluster() -> str:
    response = client.post(
        "/v1/clusters",
        json={
            "documents": [
                {
                    "documentId": "stream-doc-a",
                    "sourceUrl": "https://example.com/stream-a",
                    "title": "Streaming reasoning models",
                    "excerpt": "Compact models improve local inference.",
                    "entities": ["reasoning", "inference"],
                },
                {
                    "documentId": "stream-doc-b",
                    "sourceUrl": "https://example.com/stream-b",
                    "title": "Efficient inference for edge devices",
                    "excerpt": "Local model deployments become practical.",
                    "entities": ["reasoning", "inference"],
                },
            ]
        },
    )
    return response.json()["clusters"][0]["clusterId"]


def test_brief_stream_emits_ordered_sse_events() -> None:
    cluster_id = _create_cluster()

    response = client.get(f"/v1/briefs/{cluster_id}/stream")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    events = [json.loads(block.split("data: ", 1)[1]) for block in response.text.strip().split("\n\n") if block]
    assert [event["type"] for event in events] == ["meta", "claim", "done"]
    assert events[1]["evidenceCount"] == 2


def test_brief_stream_emits_error_for_unknown_cluster() -> None:
    response = client.get("/v1/briefs/missing-cluster/stream")

    assert response.status_code == 200
    assert json.loads(response.text.split("data: ", 1)[1].split("\n", 1)[0]) == {
        "type": "error",
        "code": "CLUSTER_NOT_FOUND",
    }
