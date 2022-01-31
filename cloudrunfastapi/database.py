from contextlib import contextmanager
from typing import Generator

from sqlmodel import MetaData, Session, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from cloudrunfastapi.apienv import apienv

# TODO: these should not have to be set
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
engine = create_engine(apienv.DATABASE_URL, pool_pre_ping=True)
metadata = MetaData(naming_convention=NAMING_CONVENTION)


@contextmanager
def db_session() -> Generator:
    yield Session(autoflush=True, bind=engine)
