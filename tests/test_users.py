import copy
import uuid

from config import get_logger
from schemas.user import BIO_CHAR_LIMIT
from tests.factories.user import (test_user_alice, test_user_alice_update,
                                  test_user_bob)

logger = get_logger()


def test_no_users(client):
    response = client.get(f"/users")
    assert response.status_code == 400


def test_no_user(client):
    response = client.get(f"/users/{str(uuid.uuid4())}")
    assert response.status_code == 400


def test_user_create(client):
    response = client.post("/users", json=test_user_bob)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data.get('id')
    assert response_data.get('name') == 'Bob Smith'
    assert response_data.get('created_at')
    assert response_data.get('updated_at')
    assert not response_data.get('deleted_at')


def test_users_get(client):
    response = client.get(f"/users")
    response_data = response.json()
    assert response.status_code == 200
    assert len(response_data) == 1

    first_user_id = response_data[0].get('id')
    response = client.get(f"/users/{first_user_id}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == first_user_id
    assert response_data.get('name') == 'Bob Smith'


def test_user_update(client):
    response = client.post("/users", json=test_user_alice)
    response_data = response.json()
    assert response.status_code == 200

    user_id = response_data.get('id')
    response = client.put(f"/users/{user_id}", json=test_user_alice_update)
    print(response.json())
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == user_id
    assert response_data.get('name') == 'Alice Smith'
    assert response_data.get('bio') == 'metrics #puns'


def test_user_update_missing(client):
    response = client.put(f"/users/{str(uuid.uuid4())}", json=test_user_bob)
    assert response.status_code == 400


def test_bio_over_char_limit(client):
    test_over_limit = copy.copy(test_user_bob)
    test_over_limit['bio'] = 'a' * (BIO_CHAR_LIMIT + 1)
    response = client.post("/users", json=test_over_limit)
    assert response.status_code == 422
