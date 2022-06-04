import copy
import uuid

from starlette.testclient import TestClient

from cloudrunfastapi.models import UserCreate, UserUpdate
from tests.mocks import MockAuth, MockUsers

mock_auth = MockAuth()
mock_user_bob_dict = UserCreate.Config.schema_extra["example"]
mock_user_bob_update_dict = UserUpdate.Config.schema_extra["example"]
mock_user_alice_dict = MockUsers.mock_user_alice


def test_create_user(client: TestClient) -> None:
    response = client.post("/users", json=mock_user_bob_dict)
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("created_at") and body.get("updated_at")
    assert body.get("name") == "Bob Smith"
    assert body.get("items") == []


def test_create_user_no_duplicate_emails(client: TestClient) -> None:
    response = client.post("/users", json=mock_user_bob_dict)
    assert response.status_code == 422


def test_get_user(client: TestClient) -> None:
    response = client.post("/users", json=mock_user_alice_dict)
    assert response.status_code == 200
    body = response.json()
    id = body.get("id")
    response = client.get(
        f"/users/{id}",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("email") == "alice@example.com"
    assert body.get("created_at") and body.get("updated_at")


def test_get_user_missing(client: TestClient) -> None:
    response = client.get(
        f"/users/{uuid.uuid4()}",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 400


def test_list_users(client: TestClient) -> None:
    response = client.get(
        "/users",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_update_user(client: TestClient) -> None:
    response = client.put(
        "/users",
        json=mock_user_bob_update_dict,
        headers=mock_auth.mock_auth_header(mock_user_bob_dict, client),
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("created_at") < body.get("updated_at")
    assert body.get("name") == "Robert Smith"
    assert body.get("email") == "new@example.io"


def test_update_user_no_duplicate_emails(client: TestClient) -> None:
    response = client.put(
        "/users",
        json=mock_user_bob_update_dict,
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 422


def test_delete_user(client: TestClient) -> None:
    response = client.post(
        "/users",
        json={
            "name": "Another User",
            "email": "anotheruser@example.com",
            "password_hash": "Th3secret_",
            "bio": "logy #puns",
        },
    )
    assert response.status_code == 200

    response = client.get(
        "/users",
        headers=mock_auth.mock_auth_header(
            {
                "name": "Another User",
                "email": "anotheruser@example.com",
                "password_hash": "Th3secret_",
                "bio": "logy #puns",
            },
            client,
        ),
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3

    response = client.delete(
        "/users",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200

    response = client.get(
        "/users",
        headers=mock_auth.mock_auth_header(
            {
                "name": "Another User",
                "email": "anotheruser@example.com",
                "password_hash": "Th3secret_",
                "bio": "logy #puns",
            },
            client,
        ),
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_bio_too_long(client: TestClient) -> None:
    mock_user = copy.copy(mock_user_bob_dict)
    mock_user["bio"] = "?" * 100 * 100
    response = client.post("/users", json=mock_user)
    assert response.status_code == 422
    assert response.json().get("detail")[0].get("msg") == "Bio is too long."


def test_bad_password(client: TestClient) -> None:
    mock_user = copy.copy(mock_user_bob_dict)
    mock_user["password_hash"] = "short"
    response = client.post("/users", json=mock_user)
    assert response.status_code == 422
    assert response.json().get("detail") == (
        "Password must be 8 characters or more and have a mix of uppercase, "
        "lowercase, numbers, and special characters."
    )
