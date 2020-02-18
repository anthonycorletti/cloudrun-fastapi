# import pytest
import gunicorn_config
from config import get_logger

logger = get_logger()


def test_placeholder(client):
    logger.debug('a little debug message')
    assert True


def test_healthcheck(client):
    response = client.get('/health')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get('message') == 'alive and kicking'


def test_gunicorn_config_worker_class(client):
    assert gunicorn_config.worker_class == 'uvicorn.workers.UvicornWorker'
