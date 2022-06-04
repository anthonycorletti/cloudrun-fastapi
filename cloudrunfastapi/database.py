from typing import Generator

from sqlmodel import Session, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from cloudrunfastapi.apienv import apienv
from cloudrunfastapi.logger import logger

# TODO: these should not have to be set
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

engine = create_engine(
    url=apienv.DATABASE_URL,
    pool_size=apienv.DB_POOL_SIZE,
    max_overflow=apienv.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)


def get_db() -> Generator:
    db = Session(
        autoflush=True,
        autocommit=False,
        bind=engine,
    )
    try:
        logger.debug("yielding db")
        yield db
        logger.debug("yielded db")
    finally:
        logger.debug("closing db")
        db.close()
        logger.debug("db closed")
