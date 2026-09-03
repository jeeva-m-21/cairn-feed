from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_brief_rejects_unknown_cluster() -> None:
    response = client.post("/v1/briefs", json={"clusterId": "not-a-real-cluster"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Cluster not found"
