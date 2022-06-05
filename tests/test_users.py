import uuid
from typing import Dict

from starlette.testclient import TestClient

from tests.conftest import mock_auth_header


def test_create_user(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "newuser@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("created_at") and body.get("updated_at")
    assert body.get("name") == "Firstname Lastname"
    assert body.get("email") == "newuser@example.com"
    assert body.get("items") == []


def test_create_user_no_duplicate_emails(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "noduplicates@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200
    response = client.post("/users", json=_user_data)
    assert response.status_code == 422


def test_get_user(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "getthisuser@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200
    body = response.json()
    id = body.get("id")
    response = client.get(
        f"/users/{id}",
        headers=mock_auth_header(client=client, user_data=_user_data),
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("email") == "getthisuser@example.com"
    assert body.get("created_at") and body.get("updated_at")


def test_get_user_missing(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "getmissing@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200
    response = client.get(
        f"/users/{uuid.uuid4()}",
        headers=mock_auth_header(client=client, user_data=_user_data),
    )
    assert response.status_code == 400


def test_list_users(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "listusers@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200
    response = client.get(
        "/users",
        headers=mock_auth_header(client=client, user_data=_user_data),
    )
    assert response.status_code == 200
    body = response.json()
    assert type(body) == list


def test_update_user(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "updateme@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "updateme@example.com"
    _update_body = user_data.copy()
    _update_body["email"] = "newemail@example.com"
    response = client.put(
        "/users",
        json=_update_body,
        headers=mock_auth_header(client=client, user_data=_user_data),
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("created_at") < body.get("updated_at")
    assert body.get("email") == "newemail@example.com"


def test_update_user_no_duplicate_emails(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "canttouchthis@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200

    _user_data = user_data.copy()
    _user_data["email"] = "tryingtotouchthis@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "tryingtotouchthis@example.com"

    _update_body = user_data.copy()
    _update_body["email"] = "canttouchthis@example.com"
    response = client.put(
        "/users",
        json=_update_body,
        headers=mock_auth_header(client=client, user_data=_user_data),
    )
    assert response.status_code == 422
    assert response.json().get("detail") == "This email is taken. Try another."


def test_delete_user(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "deleteme@example.com"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 200

    response = client.delete(
        "/users", headers=mock_auth_header(client=client, user_data=_user_data)
    )
    assert response.status_code == 200


def test_bio_too_long(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["bio"] = "?" * 100 * 100
    response = client.post("/users", json=_user_data)
    assert response.status_code == 422
    assert response.json().get("detail")[0].get("msg") == "Bio is too long."


def test_bad_password(client: TestClient, user_data: Dict) -> None:
    _user_data = user_data.copy()
    _user_data["email"] = "badpass@example.com"
    _user_data["password_hash"] = "short"
    response = client.post("/users", json=_user_data)
    assert response.status_code == 422
    assert response.json().get("detail") == (
        "Password must be 8 characters or more and have a mix of uppercase, "
        "lowercase, numbers, and special characters."
    )
