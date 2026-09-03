from typing import Any

from fastapi.testclient import TestClient

from cairn_api.main import app

client = TestClient(app)


def test_create_profile_returns_id_and_defaults() -> None:
    response = client.post("/v1/profile")

    assert response.status_code == 201
    payload = response.json()
    assert "profileId" in payload
    assert payload["topics"] == []
    assert payload["experienceLevel"] == "intermediate"
    assert payload["readingStyle"] == "briefing"
    assert payload["facets"] == []


def test_get_profile_returns_saved_data() -> None:
    create_response = client.post(
        "/v1/profile",
        json={
            "topics": ["llms", "agents"],
            "experienceLevel": "advanced",
            "readingStyle": "deep_dive",
            "facets": ["research", "coding"],
        },
    )

    profile_id = create_response.json()["profileId"]
    get_response = client.get(f"/v1/profile/{profile_id}")

    assert get_response.status_code == 200
    payload = get_response.json()
    assert payload["profileId"] == profile_id
    assert payload["topics"] == ["llms", "agents"]
    assert payload["experienceLevel"] == "advanced"


def test_feed_respects_profile_topics_for_relevance() -> None:
    profile_response = client.post(
        "/v1/profile",
        json={"topics": ["agents"], "experienceLevel": "intermediate"},
    )
    profile_id = profile_response.json()["profileId"]

    feed_response = client.get(f"/v1/feed?section=for_you&profileId={profile_id}")

    assert feed_response.status_code == 200
    payload = feed_response.json()
    assert payload["section"] == "for_you"
    assert len(payload["items"]) >= 1
    assert any("agents" in item["relevanceReason"].lower() for item in payload["items"])