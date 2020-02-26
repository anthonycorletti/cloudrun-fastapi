import uuid

import pytest

from config import get_logger
from tests.factories.item import test_item, updated_test_item

logger = get_logger()


def test_no_items(client):
    response = client.get(f"/items")
    assert response.status_code == 400


def test_no_item(client):
    response = client.get(f"/items/{str(uuid.uuid4())}")
    assert response.status_code == 400


def test_item_create(client):
    response = client.post("/items", json=test_item)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data.get('id')
    assert response_data.get('name') == 'Item name'
    assert response_data.get('description') == 'Item description'
    assert response_data.get('created_at')
    assert response_data.get('updated_at')
    assert not response_data.get('deleted_at')


def test_item_get(client):
    response = client.post("/items", json=test_item)
    response_data = response.json()
    assert response.status_code == 200

    item_id = response_data.get('id')
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == item_id


def test_items_get(client):
    response = client.get(f"/items")
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 2


def test_item_update(client):
    response = client.post("/items", json=test_item)
    response_data = response.json()
    assert response.status_code == 200

    item_id = response_data.get('id')
    response = client.put(f"/items/{item_id}", json=updated_test_item)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == item_id
    assert response_data.get('name') == 'Updated item name'


def test_item_update_missing(client):
    response = client.put(f"/items/{str(uuid.uuid4())}",
                          json=updated_test_item)
    assert response.status_code == 400
