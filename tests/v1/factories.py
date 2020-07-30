import base64
import json

from starlette.testclient import TestClient

from config import project_id


class ItemFactory:
    mock_item = {"name": "Item name", "description": "Item description"}
    updated_mock_item = {
        "name": "Updated item name",
        "description": "Updated item description"
    }


class UserFactory:
    mock_user_bob = {
        "name": "Bob Smith",
        "email": "bob@example.com",
        "password": "Thes3cret_",
        "bio": "logy #puns"
    }

    mock_user_bob_update = {
        "name": "Robert Smith",
        "email": "robert@example.io",
        "bio": "metrics #puns"
    }

    mock_user_alice = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "password": "Thes3cret_",
        "bio": "logy #puns"
    }

    mock_user_charlie = {
        "name": "Charlie Smith",
        "email": "charlie@example.com",
        "password": "Thes3cret_",
        "bio": "logy #puns"
    }


class AuthFactory:
    def mock_auth_header(self, user_data: dict, client: TestClient) -> dict:
        oauth_form = {
            "username": user_data.get("email"),
            "password": user_data.get("password")
        }
        response = client.post("/v1/login", data=oauth_form)
        return {
            "Authorization": f"Bearer {response.json().get('access_token')}"
        }

    def mock_auth_header_bad(self) -> dict:
        return {"Authorization": "Bearer smash"}


class PubsubFactory:
    def mock_encoded_pubsub_message(self, data: dict, sub_name: str) -> bytes:
        bytes = json.dumps(data).encode('utf8')
        encoded_data = base64.b64encode(bytes).decode('utf8')
        result = {
            "message": {
                "data": encoded_data,
            },
            "subscription": f"projects/{project_id}/subscriptions/{sub_name}"
        }
        return json.dumps(result).encode('utf8')

    def mock_encoded_pubsub_message_no_data(self, data: dict,
                                            sub_name: str) -> bytes:
        bytes = json.dumps(data).encode('utf8')
        encoded_data = base64.b64encode(bytes).decode('utf8')
        result = {
            "message": {
                "notdata": encoded_data,
            },
            "subscription": f"projects/{project_id}/subscriptions/{sub_name}"
        }
        return json.dumps(result).encode('utf8')
