import importlib
import os
from pathlib import Path

import pytest

import config
import gunicorn_config
from config import get_logger

logger = get_logger()
PROJECT_ID = Path('tmp/project_id').read_text().strip()


def test_placeholder():
    logger.debug('a little debug message')
    assert True


def test_healthcheck(client):
    response = client.get('/health')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get('message') == 'alive and kicking'


def test_gunicorn_config_worker_class():
    assert gunicorn_config.worker_class == 'uvicorn.workers.UvicornWorker'


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_remote_config_locally():
    unset_env_project_id = False
    if not os.environ.get('PROJECT_ID'):
        os.environ['PROJECT_ID'] = PROJECT_ID
        importlib.reload(config)
        unset_env_project_id = True
    assert config.secrets.DATABASE_URL == 'postgresql+psycopg2://postgres@postgres:5432/postgres_test_db'
    if unset_env_project_id:
        del os.environ['PROJECT_ID']
        importlib.reload(config)


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_local_config_remotely():
    project_id = os.environ.get('PROJECT_ID')
    if project_id:
        del os.environ['PROJECT_ID']
        importlib.reload(config)
    assert config.secrets.DATABASE_URL == 'postgresql+psycopg2://postgres@localhost:5432/postgres_test_db'
    if project_id:
        os.environ['PROJECT_ID'] = project_id
        importlib.reload(config)
