from starlette.testclient import TestClient


class MockAuth:
    def mock_auth_header(self, user_data: dict, client: TestClient) -> dict:
        oauth_form = {
            "username": user_data.get("email"),
            "password": user_data.get("password"),
        }
        response = client.post("/login", data=oauth_form)
        return {"Authorization": f"Bearer {response.json().get('access_token')}"}


class MockUsers:
    mock_user_alice = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "password": "Thes3cret_",
        "bio": "logy #puns",
    }
