import copy
import uuid

from schemas.user import BIO_CHAR_LIMIT
from tests.factories.user import (mock_user_alice, mock_user_bob,
                                  mock_user_bob_update)
from tests.helpers import headers


def test_user_create_get(client):
    response = client.post("/users", json=mock_user_bob)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data.get('id')
    assert response_data.get('name') == 'Bob Smith'
    assert response_data.get('created_at')
    assert response_data.get('updated_at')

    user_id = response_data.get('id')
    response = client.get(f"/users/{user_id}",
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 200

    response = client.post("/users", json=mock_user_alice)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data.get('id')
    assert response_data.get('name') == 'Alice Smith'
    assert response_data.get('created_at')
    assert response_data.get('updated_at')

    response = client.get("/users", headers=headers(client, mock_user_bob))
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_user_create_fail_preexisting_email(client):
    response = client.post("/users", json=mock_user_bob)
    assert response.status_code == 422
    assert response.json().get('detail') == 'This email is taken. Try another.'


def update_user_same_total(client):
    response = client.put("/users",
                          json=mock_user_bob_update,
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 200
    response = client.get("/users", headers=headers(client, mock_user_bob))
    assert len(response.json()) == 2


def test_no_user(client):
    response = client.get(f"/users/{str(uuid.uuid4())}",
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 400


def test_user_update(client):
    # update user, assert that the same number of users exist
    response = client.put("/users",
                          json=mock_user_bob_update,
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 200
    assert response.json().get('email') == 'robert@example.io'
    assert response.json().get('name') == 'Robert Smith'

    # update user email's already taken
    response = client.put("/users",
                          json=mock_user_alice,
                          headers=headers(client, mock_user_bob))
    assert response.status_code == 422


def test_user_create_invalid_pass(client):
    data = copy.copy(mock_user_bob)
    data['email'] = 'test@example.com'
    for badpass in ['noupper', 'NOLOWER', 'nospecial', 'short', '']:
        data['password'] = badpass
        response = client.post("/users", json=data)
        assert response.status_code == 422


def test_bio_over_char_limit(client):
    test_over_limit = copy.copy(mock_user_bob)
    test_over_limit['bio'] = 'a' * (BIO_CHAR_LIMIT + 1)
    response = client.post("/users", json=test_over_limit)
    assert response.status_code == 422


def test_user_delete(client):
    response = client.delete(f'/users', headers=headers(client, mock_user_bob))
    assert response.status_code == 200
