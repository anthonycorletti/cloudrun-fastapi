import uuid

from starlette.testclient import TestClient

from cloudrunfastapi.schemas.item import ItemCreate, ItemUpdate
from cloudrunfastapi.schemas.user import UserCreate
from tests.mocks import MockAuth, MockUsers

mock_auth = MockAuth()
mock_user_bob_dict = UserCreate.Config.schema_extra["example"]
mock_user_alice_dict = MockUsers.mock_user_alice
mock_item_dict = ItemCreate.Config.schema_extra["example"]
mock_item_updated_dict = ItemUpdate.Config.schema_extra["example"]


def test_no_items(client: TestClient) -> None:
    response = client.post("/users", json=mock_user_bob_dict)
    assert response.status_code == 200

    response = client.get(
        "/items",
        headers=mock_auth.mock_auth_header(mock_user_bob_dict, client),
    )
    assert response.status_code == 400


def test_create_item(client: TestClient) -> None:
    response = client.post("/users", json=mock_user_alice_dict)
    assert response.status_code == 200
    user_id = response.json().get("id")

    response = client.post(
        "/items",
        json=mock_item_dict,
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("created_at") and body.get("updated_at")
    assert body.get("name") == "Item name"
    assert body.get("user_id") == user_id


def test_get_item(client: TestClient) -> None:
    response = client.post(
        "/items",
        json=mock_item_dict,
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    id = response.json().get("id")

    response = client.get(
        f"/items/{id}",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("name") == "Item name"


def test_no_item(client: TestClient) -> None:
    response = client.get(
        f"/items/{uuid.uuid4()}",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 400


def test_no_item_update(client: TestClient) -> None:
    response = client.put(
        f"/items/{uuid.uuid4()}",
        json=mock_item_dict,
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 400


def test_no_item_delete(client: TestClient) -> None:
    response = client.delete(
        f"/items/{uuid.uuid4()}",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 400


def test_list_items(client: TestClient) -> None:
    response = client.get(
        "/items",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_update_item(client: TestClient) -> None:
    response = client.post(
        "/items",
        json=mock_item_dict,
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    id = response.json().get("id")
    user_id = response.json().get("user_id")

    response = client.put(
        f"/items/{id}",
        json=mock_item_updated_dict,
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("user_id") == user_id
    assert body.get("created_at") < body.get("updated_at")
    assert body.get("name") == "Updated item name"


def test_delete_item(client: TestClient) -> None:
    response = client.get(
        "/items",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3
    id = body[0].get("id")

    response = client.delete(
        f"/items/{id}",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200

    response = client.get(
        "/items",
        headers=mock_auth.mock_auth_header(mock_user_alice_dict, client),
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert id not in [el.get("id") for el in body]
