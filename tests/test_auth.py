from starlette.testclient import TestClient

from cloudrunfastapi.models import UserCreate
from tests.mocks import MockAuth

mock_auth = MockAuth()
mock_user_bob_dict = UserCreate.Config.schema_extra["example"]


def test_unauthorized(client: TestClient) -> None:
    response = client.post("/users", json=mock_user_bob_dict)
    assert response.status_code == 200

    response = client.post(
        "/login", data={"username": "user@example.com", "password": "nope"}
    )
    assert response.status_code == 401


def test_unauthorized_unknown(client: TestClient) -> None:
    response = client.post(
        "/login", data={"username": "phil@example.com", "password": "incorrect"}
    )
    assert response.status_code == 401


def test_logout(client: TestClient) -> None:
    response = client.post(
        "/logout",
        headers=mock_auth.mock_auth_header(mock_user_bob_dict, client),
    )
    assert response.status_code == 200
    assert not response.json().get("access_token")


def test_token_no_user(client: TestClient) -> None:
    response = client.get("/items", headers=mock_auth.mock_auth_header({}, client))
    assert response.status_code == 401
