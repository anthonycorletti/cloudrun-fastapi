import uuid
from typing import Dict

from starlette.testclient import TestClient


def test_no_items(client: TestClient, headers: Dict) -> None:
    response = client.get("/items", headers=headers)
    assert response.status_code == 400


def test_create_item(client: TestClient, item_data: Dict, headers: Dict) -> None:
    response = client.get("/current_user", headers=headers)
    user_id = response.json().get("id")
    item_data["user_id"] = user_id
    response = client.post("/items", json=item_data, headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body.get("id")
    assert body.get("created_at") and body.get("updated_at")
    assert body.get("name") == "A New Item"
    assert body.get("user_id") == user_id


def test_get_item(client: TestClient, item_data: Dict, headers: Dict) -> None:
    response = client.get("/current_user", headers=headers)
    user_id = response.json().get("id")
    item_data["user_id"] = user_id

    response = client.post("/items", json=item_data, headers=headers)
    assert response.status_code == 200
    id = response.json().get("id")

    response = client.get(f"/items/{id}", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("name") == "A New Item"


def test_no_item(client: TestClient, headers: Dict) -> None:
    response = client.get(f"/items/{uuid.uuid4()}", headers=headers)
    assert response.status_code == 400


def test_no_item_update(client: TestClient, item_data: Dict, headers: Dict) -> None:
    _item_data = item_data.copy()
    _item_data = {**_item_data, "name": "A New Item"}
    response = client.put(f"/items/{uuid.uuid4()}", json=_item_data, headers=headers)
    assert response.status_code == 400


def test_no_item_delete(client: TestClient, headers: Dict) -> None:
    response = client.delete(f"/items/{uuid.uuid4()}", headers=headers)
    assert response.status_code == 400


def test_list_items(client: TestClient, item_data: Dict, headers: Dict) -> None:
    response = client.get("/current_user", headers=headers)
    user_id = response.json().get("id")
    item_data["user_id"] = user_id
    response = client.post("/items", json=item_data, headers=headers)
    assert response.status_code == 200
    response = client.get("/items", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert type(body) == list
    assert len(body) > 0


def test_update_item(client: TestClient, item_data: Dict, headers: Dict) -> None:
    response = client.get("/current_user", headers=headers)
    user_id = response.json().get("id")
    item_data["user_id"] = user_id
    response = client.post("/items", json=item_data, headers=headers)
    assert response.status_code == 200

    id = response.json().get("id")
    user_id = response.json().get("user_id")
    _item_data = item_data.copy()
    _item_data["name"] = "A New New Item"
    response = client.put(f"/items/{id}", json=_item_data, headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body.get("id") == id
    assert body.get("user_id") == user_id
    assert body.get("created_at") < body.get("updated_at")
    assert body.get("name") == "A New New Item"


def test_delete_item(client: TestClient, item_data: Dict, headers: Dict) -> None:
    response = client.get("/current_user", headers=headers)
    user_id = response.json().get("id")
    item_data["user_id"] = user_id
    response = client.post("/items", json=item_data, headers=headers)
    assert response.status_code == 200
    item_id = response.json().get("id")
    response = client.delete(f"/items/{item_id}", headers=headers)
    assert response.status_code == 200
