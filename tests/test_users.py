import copy
import uuid
from datetime import datetime

from config import get_logger
from schemas.user import BIO_CHAR_LIMIT
from tests.factories.user import (test_user_alice, test_user_bob,
                                  test_user_bob_update)

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


def test_user_create_get_update(client):
    response = client.post("/users", json=test_user_bob)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data.get('id')
    assert response_data.get('name') == 'Bob Smith'
    assert response_data.get('created_at')
    assert response_data.get('updated_at')
    assert not response_data.get('deleted_at')

    user_id = response_data.get('id')
    response = client.get(f"/users/{user_id}", headers=headers(client))
    assert response.status_code == 200

    assert response.status_code == 200
    assert response_data.get('id')
    assert response_data.get('name') == 'Bob Smith'
    assert response_data.get('created_at')
    assert response_data.get('updated_at')
    assert not response_data.get('deleted_at')

    response = client.put(f"/users/{user_id}",
                          json=test_user_bob_update,
                          headers=headers(client))
    assert response.status_code == 200

    response_data = response.json()
    assert response_data.get('id') == user_id
    assert response_data.get('name') == 'Robert Smith'
    assert response_data.get('bio') == 'metrics #puns'


def test_no_user(client):
    response = client.get(f"/users/{str(uuid.uuid4())}",
                          headers=headers(client))
    assert response.status_code == 404


def test_user_create_invalid_pass(client):
    data = copy.copy(test_user_bob)
    data['email'] = 'test@example.com'
    for badpass in ['noupper', 'NOLOWER', 'nospecial', 'short', '']:
        data['password'] = badpass
        response = client.post("/users", json=data)
        assert response.status_code == 422


def test_user_create_fail_preexisting_email(client):
    response = client.post("/users", json=test_user_bob)
    assert response.status_code == 400
    assert response.json().get(
        'detail') == 'An account already exists with this email.'


def test_user_update_wrong_user(client):
    response = client.put(f"/users/{str(uuid.uuid4())}",
                          json=test_user_bob,
                          headers=headers(client))
    assert response.status_code == 401


def test_bio_over_char_limit(client):
    test_over_limit = copy.copy(test_user_bob)
    test_over_limit['bio'] = 'a' * (BIO_CHAR_LIMIT + 1)
    response = client.post("/users", json=test_over_limit)
    assert response.status_code == 422


def test_user_delete(client):
    response = client.post("/users", json=test_user_alice)
    assert response.status_code == 200

    user_id = response.json().get('id')
    oauth_form = {
        'username': test_user_alice.get('email'),
        'password': test_user_alice.get('password')
    }
    response = client.post("/token", data=oauth_form)
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    access_token = response.json().get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.delete(f'/users/{user_id}',
                             json={'deleted_at': str(datetime.now())},
                             headers=headers)
    assert response.status_code == 200


def test_user_delete_wrong_user(client):
    test_user_alice['email'] = 'alice2@example.com'
    response = client.post("/users", json=test_user_alice)
    assert response.status_code == 200

    user_id = response.json().get('id')
    oauth_form = {
        'username': test_user_bob.get('email'),
        'password': test_user_bob.get('password')
    }
    response = client.post("/token", data=oauth_form)
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    access_token = response.json().get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.delete(f'/users/{user_id}',
                             json={'deleted_at': str(datetime.now())},
                             headers=headers)
    assert response.status_code == 401
