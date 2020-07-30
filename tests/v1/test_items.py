import uuid

from tests.v1.factories import AuthFactory, ItemFactory, UserFactory

af = AuthFactory()


def test_no_items(client):
    response = client.post("/v1/users", json=UserFactory.mock_user_bob)
    assert response.status_code == 200

    response = client.get("/v1/items",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_bob, client))
    assert response.status_code == 400


def test_create_item(client):
    response = client.post("/v1/users", json=UserFactory.mock_user_alice)
    assert response.status_code == 200
    user_id = response.json().get("id")

    response = client.post("/v1/items",
                           json=ItemFactory.mock_item,
                           headers=af.mock_auth_header(
                               UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("created_at") and body.get("updated_at")
    assert body.get("name") == "Item name"
    assert body.get("user_id") == user_id


def test_get_item(client):
    response = client.post("/v1/items",
                           json=ItemFactory.mock_item,
                           headers=af.mock_auth_header(
                               UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    id = response.json().get("id")

    response = client.get(f"/v1/items/{id}",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("name") == "Item name"


def test_no_item(client):
    response = client.get(f"/v1/items/{uuid.uuid4()}",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 400


def test_no_item_update(client):
    response = client.put(f"/v1/items/{uuid.uuid4()}",
                          json=ItemFactory.mock_item,
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 400


def test_no_item_delete(client):
    response = client.delete(f"/v1/items/{uuid.uuid4()}",
                             headers=af.mock_auth_header(
                                 UserFactory.mock_user_alice, client))
    assert response.status_code == 400


def test_list_items(client):
    response = client.get("/v1/items",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_update_item(client):
    response = client.post("/v1/items",
                           json=ItemFactory.mock_item,
                           headers=af.mock_auth_header(
                               UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    id = response.json().get("id")
    user_id = response.json().get("user_id")

    response = client.put(f"/v1/items/{id}",
                          json=ItemFactory.updated_mock_item,
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("user_id") == user_id
    assert body.get("created_at") < body.get("updated_at")
    assert body.get("name") == "Updated item name"


def test_delete_item(client):
    response = client.get("/v1/items",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3
    id = body[0].get("id")

    response = client.delete(f"/v1/items/{id}",
                             headers=af.mock_auth_header(
                                 UserFactory.mock_user_alice, client))
    assert response.status_code == 200

    response = client.get("/v1/items",
                          headers=af.mock_auth_header(
                              UserFactory.mock_user_alice, client))
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert id not in [el.get("id") for el in body]
