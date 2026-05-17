from __future__ import annotations


def test_signup(client):
    response = client.post(
        "/api/auth/signup",
        json={"username": "newuser", "email": "new@example.com", "password": "password123"},
    )

    assert response.status_code == 201
    assert response.get_json()["username"] == "newuser"


def test_login(client, test_user):
    response = client.post(
        "/api/auth/login",
        json={"username": test_user["username"], "password": "password123"},
    )

    data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in data
    assert data["username"] == test_user["username"]


def test_me(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.get_json()["username"] == "testuser"
