from starlette.testclient import TestClient


def test_healthcheck(client: TestClient) -> None:
    response = client.get("/healthcheck")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("message") == "We're on the air."
