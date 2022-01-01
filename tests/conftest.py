import logging
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.config import environ
from starlette.testclient import TestClient

from alembic import command
from alembic.config import Config
from cloudrunfastapi.apienv import apienv
from cloudrunfastapi.main import api

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.
environ["TESTING"] = "True"
logging.getLogger("alembic").setLevel(logging.ERROR)


@pytest.fixture(scope="module", autouse=True)
def create_test_database() -> Generator:
    dburl = apienv.DATABASE_URL

    if database_exists(dburl):
        logging.info(  # pragma: no cover
            "Test database already exists ... "
            "Dropping and recreating the test database."
        )
        drop_database(dburl)  # pragma: no cover

    create_engine(dburl)
    create_database(dburl)
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")
    yield
    drop_database(dburl)


@pytest.fixture()
def client() -> Generator:
    with TestClient(api) as client:
        yield client
