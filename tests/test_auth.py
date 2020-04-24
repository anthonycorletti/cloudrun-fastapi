import uuid
from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer

from actions.auth import create_access_token
from tests.factories.user import mock_user_bob
from tests.helpers import create_test_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def test_oauth_token_bad_user(client):
    oauth_form = {
        'username': mock_user_bob.get('email'),
        'password': mock_user_bob.get('password')
    }
    response = client.post("/login", data=oauth_form)
    assert response.status_code == 401
    assert response.json().get('detail') == "Incorrect login credentials."


def test_oauth_token_current_user(client):
    create_test_user(client, mock_user_bob)
    oauth_form = {
        'username': mock_user_bob.get('email'),
        'password': mock_user_bob.get('password')
    }
    response = client.post("/login", data=oauth_form)
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    access_token = response.json().get('access_token')

    response = client.get('/current_user',
                          headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json().get('email') == 'bob@example.com'


def test_oauth_token_invalid_pass(client):
    oauth_form = {
        'username': mock_user_bob.get('email'),
        'password': mock_user_bob.get('password') + 'invalid_pass'
    }
    response = client.post("/login", data=oauth_form)
    assert response.status_code == 401


def test_get_current_user_garbage_token(client):
    token = create_access_token(data={}, expires_delta=timedelta(minutes=50))
    response = client.get(
        '/current_user',
        headers={'Authorization': f'Bearer {token.decode("utf8")}'})
    assert response.status_code == 401


def test_get_current_user_garbage_missing_email(client):
    token = create_access_token(data={'sub': ''},
                                expires_delta=timedelta(minutes=10))
    response = client.get(
        '/current_user',
        headers={'Authorization': f'Bearer {token.decode("utf8")}'})
    assert response.status_code == 401


def test_get_current_user_expired_token(client):
    token = create_access_token(data={'sub': 'bob@example.com'},
                                expires_delta=timedelta(minutes=-1))
    response = client.get(
        '/current_user',
        headers={'Authorization': f'Bearer {token.decode("utf8")}'})
    assert response.status_code == 401


def test_get_current_user_missing_user(client):
    token = create_access_token(data={
        'id': str(uuid.uuid4()),
        'email': 'missinguser@example.com'
    },
                                expires_delta=timedelta(minutes=10))
    response = client.get(
        '/current_user',
        headers={'Authorization': f'Bearer {token.decode("utf8")}'})
    assert response.status_code == 401


def test_logout(client):
    oauth_form = {
        'username': mock_user_bob.get('email'),
        'password': mock_user_bob.get('password')
    }
    response = client.post("/login", data=oauth_form)
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    access_token = response.json().get('access_token')

    response = client.get('/current_user',
                          headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json().get('email') == 'bob@example.com'

    response = client.post("/logout",
                           headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    logout_token = response.json().get("access_token")
    response = client.get("/current_user",
                          headers={'Authorization': f'Bearer {logout_token}'})
    assert response.status_code == 401
