import base64
import json

from starlette.testclient import TestClient

from config import project_id


def create_test_user(client: TestClient, user_data: dict) -> str:
    response = client.post("/users", json=user_data)
    return response.json().get('id')


def headers(client: TestClient, user_data: dict) -> dict:
    try:
        create_test_user(client, user_data)
    except Exception:
        pass
    oauth_form = {
        'username': user_data.get('email'),
        'password': user_data.get('password')
    }
    response = client.post("/login", data=oauth_form)
    assert response.status_code == 200
    assert response.json().get('token_type') == 'bearer'
    access_token = response.json().get('access_token')
    return {'Authorization': f'Bearer {access_token}'}


def create_user_item(client: TestClient, user_data: dict,
                     item_data: dict) -> str:
    response = client.post("/items",
                           json=item_data,
                           headers=headers(client, user_data))
    assert response.status_code == 200
    return response.json().get('id')


def mock_encoded_pubsub_message(data: dict, sub_name: str) -> bytes:
    bytes = json.dumps(data).encode('utf8')
    encoded_data = base64.b64encode(bytes).decode('utf8')
    result = {
        "message": {
            "data": encoded_data,
        },
        "subscription": f"projects/{project_id}/subscriptions/{sub_name}"
    }
    return json.dumps(result).encode('utf8')


def mock_encoded_pubsub_message_no_data(data: dict, sub_name: str) -> bytes:
    bytes = json.dumps(data).encode('utf8')
    encoded_data = base64.b64encode(bytes).decode('utf8')
    result = {
        "message": {
            "notdata": encoded_data,
        },
        "subscription": f"projects/{project_id}/subscriptions/{sub_name}"
    }
    return json.dumps(result).encode('utf8')
