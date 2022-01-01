from starlette.testclient import TestClient

import cloudrunfastapi.gunicorn_config as gunicorn_config


def test_gunicorn_config(client: TestClient) -> None:
    assert gunicorn_config.worker_class == "uvicorn.workers.UvicornWorker"
