from typing import Dict

from starlette.testclient import TestClient

from tests.conftest import mock_auth_header


def test_user_unauthorized(client: TestClient, user_data: Dict) -> None:
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    response = client.post(
        "/login", data={"username": "user@example.com", "password": "nope"}
    )
    assert response.status_code == 401


def test_unauthorized_unknown(client: TestClient) -> None:
    response = client.post(
        "/login",
        data={"username": "unknown@example.com", "password": "incorrect"},
    )
    assert response.status_code == 401


def test_logout(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "other_user@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200
    response = client.post(
        "/logout",
        headers=mock_auth_header(client=client, user_data=_user_data),
    )
    assert response.status_code == 200
    assert not response.json().get("access_token")


def test_token_no_user(client: TestClient) -> None:
    response = client.get(
        "/items", headers=mock_auth_header(client=client, user_data={})
    )
    assert response.status_code == 401
