import copy
import uuid

from tests.v1.factories import AuthFactory, UserFactory

af = AuthFactory()


def test_create_user(client):
    response = client.post("/v1/users", json=UserFactory.mock_user_bob)
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("created_at") and body.get("updated_at")
    assert body.get("name") == "Bob Smith"
    assert body.get("items") == []


def test_create_user_no_duplicate_emails(client):
    response = client.post("/v1/users", json=UserFactory.mock_user_bob)
    assert response.status_code == 422


def test_get_user(client):
    response = client.post("/v1/users", json=UserFactory.mock_user_alice)
    assert response.status_code == 200
    body = response.json()
    id = body.get("id")
    response = client.get(f"/v1/users/{id}",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("email") == "alice@example.com"
    assert body.get("created_at") and body.get("updated_at")


def test_get_user_missing(client):
    response = client.get(f"/v1/users/{uuid.uuid4()}",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 400


def test_list_users(client):
    response = client.get("/v1/users",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_update_user(client):
    response = client.put("/v1/users",
                          json=UserFactory.mock_user_bob_update,
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_bob, client))
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("created_at") < body.get("updated_at")
    assert body.get("name") == "Robert Smith"
    assert body.get("email") == "robert@example.io"


def test_update_user_no_duplicate_emails(client):
    response = client.put("/v1/users",
                          json=UserFactory.mock_user_bob_update,
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 422


def test_delete_user(client):
    response = client.post("/v1/users", json=UserFactory.mock_user_charlie)
    assert response.status_code == 200

    response = client.get("/v1/users",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_charlie, client))
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3

    response = client.delete("/v1/users",
                             headers=af.mock_auth_header(
                                 UserFactory.mock_user_alice, client))
    assert response.status_code == 200

    response = client.get("/v1/users",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_charlie, client))
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_bio_too_long(client):
    mock_user = copy.copy(UserFactory.mock_user_bob)
    mock_user["bio"] = "?" * 161
    response = client.post("/v1/users", json=mock_user)
    assert response.status_code == 422
    assert response.json().get("detail")[0].get("msg") == "Bio is too long."


def test_bad_password(client):
    mock_user = copy.copy(UserFactory.mock_user_bob)
    mock_user["password"] = "short"
    response = client.post("/v1/users", json=mock_user)
    assert response.status_code == 422
    assert response.json().get("detail")[0].get("msg") == (
        "Password must be 8 characters or more and have a mix of uppercase, "
        "lowercase, numbers, and special characters.")
