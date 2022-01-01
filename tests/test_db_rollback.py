import pytest
from sqlalchemy.exc import ProgrammingError
from starlette.testclient import TestClient

from cloudrunfastapi.database import db_session


def test_db_rollback(client: TestClient) -> None:
    with pytest.raises(ProgrammingError):
        with db_session() as db:
            db.execute("asdf")
