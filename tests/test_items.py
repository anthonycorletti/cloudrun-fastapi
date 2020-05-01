import uuid

from tests.factories.item import mock_item, updated_mock_item
from tests.factories.user import mock_user_alice, mock_user_bob
from tests.helpers import create_user_item, headers


def test_no_items(client):
    response = client.get(f"/items", headers=headers(client, mock_user_bob))
    assert response.status_code == 400


def test_no_item(client):
    response = client.get(f"/items/{str(uuid.uuid4())}",
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 400


def test_item_create(client):
    response = client.post("/items",
                           json=mock_item,
                           headers=headers(client, mock_user_bob))
    response_data = response.json()
    current_user = client.get("/current_user",
                              headers=headers(client, mock_user_bob))
    assert response.status_code == 200
    assert response_data.get('id')
    assert response_data.get('name') == 'Item name'
    assert response_data.get('description') == 'Item description'
    assert response_data.get('user_id') == current_user.json().get('id')
    assert response_data.get('created_at')
    assert response_data.get('updated_at')
    assert not response_data.get('deleted_at')


def test_item_get(client):
    response = client.post("/items",
                           json=mock_item,
                           headers=headers(client, mock_user_bob))
    response_data = response.json()
    assert response.status_code == 200

    item_id = response_data.get('id')
    response = client.get(f"/items/{item_id}",
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == item_id


def test_items_get(client):
    response = client.get(f"/items", headers=headers(client, mock_user_bob))
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 2


def test_item_update(client):
    response = client.post("/items",
                           json=mock_item,
                           headers=headers(client, mock_user_bob))
    response_data = response.json()
    assert response.status_code == 200

    item_id = response_data.get('id')
    response = client.put(f"/items/{item_id}",
                          json=updated_mock_item,
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == item_id
    assert response_data.get('name') == 'Updated item name'

    response = client.get(f"/items/{item_id}",
                          json=updated_mock_item,
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == item_id
    assert response_data.get('name') == 'Updated item name'

    response = client.get(f"/items", headers=headers(client, mock_user_bob))
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 3


def test_item_update_missing(client):
    response = client.put(f"/items/{str(uuid.uuid4())}",
                          json=updated_mock_item,
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 400


def test_delete_item(client):
    response = client.get(f"/items", headers=headers(client, mock_user_bob))
    response_data = response.json()
    item_id = response_data[0].get('id')

    response = client.delete(f"/items/{item_id}",
                             headers=headers(client, mock_user_bob))
    assert response.status_code == 200
    assert response.json().get('id') == item_id

    response = client.get(f"/items", headers=headers(client, mock_user_bob))
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 2


def test_delete_missing_item(client):
    response = client.delete(f"/items/{str(uuid.uuid4())}",
                             headers=headers(client, mock_user_bob))
    assert response.status_code == 400


def test_updating_other_user_item(client):
    item_id = create_user_item(client, mock_user_bob, mock_item)
    response = client.put(f"/items/{item_id}",
                          json=updated_mock_item,
                          headers=headers(client, mock_user_alice))
    assert response.status_code == 400


def test_deleting_other_user_item(client):
    item_id = create_user_item(client, mock_user_bob, mock_item)
    response = client.delete(f"/items/{item_id}",
                             headers=headers(client, mock_user_alice))
    assert response.status_code == 400
