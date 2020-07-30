import pytest
from sqlalchemy.exc import ProgrammingError

import gunicorn_config
from database import db_session


def test_gunicorn_config(client):
    assert gunicorn_config.worker_class == "uvicorn.workers.UvicornWorker"


def test_healthcheck(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("message") == "alive and kicking"


def test_db_rollback(client):
    with pytest.raises(ProgrammingError):
        with db_session() as db:
            db.execute("asdf")
