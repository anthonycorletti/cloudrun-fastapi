from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer

from actions.auth import create_access_token
from config import get_logger
from tests.factories.user import test_user_bob

logger = get_logger()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def create_test_user(client):
    response = client.post("/users", json=test_user_bob)
    return response.json().get('id')


def test_oauth_token_bad_user(client):
    oauth_form = {
        'username': test_user_bob.get('email'),
        'password': test_user_bob.get('password')
    }
    response = client.post("/token", data=oauth_form)
    assert response.status_code == 401
    assert response.json().get('detail') == "Incorrect login credentials."


def test_oauth_token_current_user(client):
    create_test_user(client)
    oauth_form = {
        'username': test_user_bob.get('email'),
        'password': test_user_bob.get('password')
    }
    response = client.post("/token", data=oauth_form)
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    access_token = response.json().get('access_token')

    response = client.get('/current_user',
                          headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json().get('email') == 'bob@example.com'


def test_oauth_token_invalid_pass(client):
    oauth_form = {
        'username': test_user_bob.get('email'),
        'password': test_user_bob.get('password') + 'invalid_pass'
    }
    response = client.post("/token", data=oauth_form)
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
    token = create_access_token(data={'sub': 'missinguser@example.com'},
                                expires_delta=timedelta(minutes=10))
    response = client.get(
        '/current_user',
        headers={'Authorization': f'Bearer {token.decode("utf8")}'})
    assert response.status_code == 401
