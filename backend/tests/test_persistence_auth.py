from fastapi.testclient import TestClient

from cairn_api.main import app


def test_profile_persistence_contract_exposes_session_cookie() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/v1/auth/dev-session",
            json={"email": "reader@example.com"},
        )

    assert response.status_code == 201
    assert "cairn_session" in response.cookies
    assert response.json()["email"] == "reader@example.com"


def test_profile_requires_session_for_persistence_boundary() -> None:
    with TestClient(app) as client:
        response = client.post("/v1/profile", json={"topics": ["agents"]})

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


def test_profile_is_not_visible_to_another_authenticated_user() -> None:
    with TestClient(app) as owner, TestClient(app) as other_user:
        owner.post("/v1/auth/dev-session", json={"email": "owner@example.com"})
        profile_id = owner.post("/v1/profile", json={"topics": ["agents"]}).json()["profileId"]

        other_user.post("/v1/auth/dev-session", json={"email": "other@example.com"})
        response = other_user.get(f"/v1/profile/{profile_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"
