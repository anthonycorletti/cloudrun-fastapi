from tests.v1.factories import AuthFactory, UserFactory

af = AuthFactory()


def test_unauthorized(client):
    response = client.post("/v1/users", json=UserFactory.mock_user_bob)
    assert response.status_code == 200

    response = client.post("/v1/login",
                           data={
                               "username": "bob@example.com",
                               "password": "nope"
                           })
    assert response.status_code == 401


def test_unauthorized_unknown(client):
    response = client.post("/v1/login",
                           data={
                               "username": "phil@example.com",
                               "password": "incorrect"
                           })
    assert response.status_code == 401


def test_logout(client):
    response = client.post("/v1/logout",
                           headers=af.mock_auth_header(
                               UserFactory.mock_user_bob, client))
    assert response.status_code == 200
    assert not response.json().get("access_token")


def test_token_no_user(client):
    response = client.get("/v1/items", headers=af.mock_auth_header({}, client))
    assert response.status_code == 401
