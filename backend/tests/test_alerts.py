from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def authenticate() -> None:
    client.post("/v1/auth/dev-session", json={"email": "alerts-tests@example.com"})


def test_create_alert_returns_alert_id() -> None:
    authenticate()
    profile_response = client.post("/v1/profile")
    profile_id = profile_response.json()["profileId"]

    alert_response = client.post(
        "/v1/alerts",
        json={"profileId": profile_id, "eventId": "evt-open-models-edge", "delivery": "email"}
    )

    assert alert_response.status_code == 201
    payload = alert_response.json()
    assert "alertId" in payload
    assert payload["profileId"] == profile_id
    assert payload["eventId"] == "evt-open-models-edge"
    assert payload["delivery"] == "email"


def test_delete_alert_removes_alert() -> None:
    authenticate()
    profile_response = client.post("/v1/profile")
    profile_id = profile_response.json()["profileId"]

    alert_response = client.post("/v1/alerts", json={"profileId": profile_id, "eventId": "evt-open-models-edge", "delivery": "email"})
    alert_id = alert_response.json()["alertId"]

    delete_response = client.delete(f"/v1/alerts/{alert_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["deleted"] == True
