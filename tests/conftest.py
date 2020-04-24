import logging

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.config import environ
from starlette.testclient import TestClient

from config import apisecrets
from main import api

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.
environ['TESTING'] = 'True'
logging.getLogger('alembic').setLevel(logging.ERROR)


@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    """
    Create a clean database on every test case.
    For safety, we should abort if a database already exists.

    We use the `sqlalchemy_utils` package here for a few helpers in
    consistently creating and dropping the database.
    """
    dburl = apisecrets.DATABASE_URL
    create_engine(dburl)
    assert not database_exists(
        dburl), 'Test database already exists. Aborting tests.'
    create_database(dburl)
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")
    # command.history(alembic_config, indicate_current=True)
    yield
    drop_database(dburl)


@pytest.fixture()
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = api.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    with TestClient(api) as client:
        yield client
