import logging
from typing import Dict, Generator

import pytest
from sqlalchemy.orm import close_all_sessions
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import create_engine
from starlette.config import environ
from starlette.testclient import TestClient

from alembic import command
from alembic.config import Config
from cloudrunfastapi.apienv import apienv
from cloudrunfastapi.main import api
from cloudrunfastapi.models import ItemCreate, UserCreate

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

    create_engine(dburl, pool_pre_ping=True)
    create_database(dburl)
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")
    yield
    close_all_sessions()
    drop_database(dburl)


@pytest.fixture()
def client() -> Generator:
    with TestClient(api) as client:
        yield client


@pytest.fixture()
def user_data() -> Dict:
    return UserCreate.Config.schema_extra["example"]


@pytest.fixture()
def item_data() -> Dict:
    return ItemCreate.Config.schema_extra["example"]


@pytest.fixture(autouse=True)
def headers() -> Dict:
    with TestClient(api) as client:
        user_data = UserCreate.Config.schema_extra["example"]
        client.post("/users", json=user_data)
        return mock_auth_header(client, user_data)


def mock_auth_header(client: TestClient, user_data: Dict) -> Dict:
    oauth_form = {
        "username": user_data.get("email"),
        "password": user_data.get("password_hash"),
    }
    response = client.post("/login", data=oauth_form)
    return {"Authorization": f"Bearer {response.json().get('access_token')}"}
