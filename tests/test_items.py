import uuid
from datetime import datetime

from config import get_logger
from tests.factories.item import test_item, updated_test_item
from tests.factories.user import test_user_alice, test_user_bob

logger = get_logger()


def create_test_user(client):
    response = client.post("/users", json=test_user_bob)
    return response.json().get('id')


def headers(client):
    try:
        create_test_user(client)
    except Exception:
        pass
    oauth_form = {
        'username': test_user_bob.get('email'),
        'password': test_user_bob.get('password')
    }
    response = client.post("/token", data=oauth_form)
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    access_token = response.json().get('access_token')
    return {'Authorization': f'Bearer {access_token}'}


def create_other_user_item(client):
    try:
        response = client.post("/users", json=test_user_alice)
        assert response.status_code == 200
    except Exception:
        pass
    oauth_form = {
        'username': test_user_alice.get('email'),
        'password': test_user_alice.get('password')
    }
    response = client.post("/token", data=oauth_form)
    assert response.status_code == 200
    access_token = response.json().get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post("/items", json=test_item, headers=headers)
    assert response.status_code == 200
    return response.json().get('id')


def test_no_items(client):
    response = client.get(f"/items", headers=headers(client))
    assert response.status_code == 400


def test_no_item(client):
    response = client.get(f"/items/{str(uuid.uuid4())}",
                          headers=headers(client))
    assert response.status_code == 400


def test_item_create(client):
    response = client.post("/items", json=test_item, headers=headers(client))
    response_data = response.json()
    current_user = client.get("/current_user", headers=headers(client))
    assert response.status_code == 200
    assert response_data.get('id')
    assert response_data.get('name') == 'Item name'
    assert response_data.get('description') == 'Item description'
    assert response_data.get('user_id') == current_user.json().get('id')
    assert response_data.get('created_at')
    assert response_data.get('updated_at')
    assert not response_data.get('deleted_at')


def test_item_get(client):
    response = client.post("/items", json=test_item, headers=headers(client))
    response_data = response.json()
    assert response.status_code == 200

    item_id = response_data.get('id')
    response = client.get(f"/items/{item_id}", headers=headers(client))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == item_id


def test_items_get(client):
    response = client.get(f"/items", headers=headers(client))
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 2


def test_item_update(client):
    response = client.post("/items", json=test_item, headers=headers(client))
    response_data = response.json()
    assert response.status_code == 200

    item_id = response_data.get('id')
    response = client.put(f"/items/{item_id}",
                          json=updated_test_item,
                          headers=headers(client))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == item_id
    assert response_data.get('name') == 'Updated item name'

    response = client.get(f"/items", headers=headers(client))
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 3


def test_item_update_missing(client):
    response = client.put(f"/items/{str(uuid.uuid4())}",
                          json=updated_test_item,
                          headers=headers(client))
    assert response.status_code == 400


def test_delete_item(client):
    response = client.get(f"/items", headers=headers(client))
    response_data = response.json()
    item_id = response_data[0].get('id')

    response = client.delete(f"/items/{item_id}",
                             json={'deleted_at': str(datetime.now())},
                             headers=headers(client))
    assert response.status_code == 200
    assert response.json().get('id') == item_id

    response = client.get(f"/items", headers=headers(client))
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 2


def test_delete_missing_item(client):
    response = client.delete(f"/items/{str(uuid.uuid4())}",
                             json={'deleted_at': str(datetime.now())},
                             headers=headers(client))
    assert response.status_code == 400


def test_updating_other_user_item(client):
    item_id = create_other_user_item(client)
    response = client.put(f"/items/{item_id}",
                          json=updated_test_item,
                          headers=headers(client))
    assert response.status_code == 401


def test_deleting_other_user_item(client):
    item_id = create_other_user_item(client)
    response = client.delete(f"/items/{item_id}",
                             json={'deleted_at': str(datetime.now())},
                             headers=headers(client))
    assert response.status_code == 401
