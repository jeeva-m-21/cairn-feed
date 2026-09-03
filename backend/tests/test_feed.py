from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_feed_returns_event_cards_in_for_you_section() -> None:
    response = client.get("/v1/feed?section=for_you")

    assert response.status_code == 200
    payload = response.json()
    assert payload["section"] == "for_you"
    assert len(payload["items"]) >= 3
    assert payload["items"][0] == {
        "id": "evt-open-models-edge",
        "title": "Open models are getting smaller without getting quiet",
        "category": "MODEL RELEASE",
        "sourceCount": 8,
        "relevanceReason": "Matches your interest in inference and open source",
    }


def test_feed_rejects_unknown_section() -> None:
    response = client.get("/v1/feed?section=unknown")

    assert response.status_code == 422
