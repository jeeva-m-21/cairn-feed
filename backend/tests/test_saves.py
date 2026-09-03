from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def authenticate() -> None:
    client.post("/v1/auth/dev-session", json={"email": "saves-tests@example.com"})


def test_save_event_returns_updated_profile_saves() -> None:
    authenticate()
    profile_response = client.post("/v1/profile")
    profile_id = profile_response.json()["profileId"]

    save_response = client.post(
        "/v1/saves",
        json={"profileId": profile_id, "eventId": "evt-open-models-edge"},
    )

    assert save_response.status_code == 201
    payload = save_response.json()
    assert payload["profileId"] == profile_id
    assert payload["saves"] == ["evt-open-models-edge"]


def test_unsave_removes_from_profile() -> None:
    authenticate()
    profile_response = client.post("/v1/profile")
    profile_id = profile_response.json()["profileId"]

    client.post("/v1/saves", json={"profileId": profile_id, "eventId": "evt-open-models-edge"})
    unsave_response = client.request(
        "DELETE",
        "/v1/saves",
        json={"profileId": profile_id, "eventId": "evt-open-models-edge"},
    )

    assert unsave_response.status_code == 200
    payload = unsave_response.json()
    assert payload["saves"] == []
