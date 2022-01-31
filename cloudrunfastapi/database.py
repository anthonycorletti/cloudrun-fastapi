from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

from cloudrunfastapi.apienv import apienv
from cloudrunfastapi.logger import logger

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=NAMING_CONVENTION)

engine = create_engine(
    apienv.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
)
SessionLocal = sessionmaker(
    autocommit=False,
    expire_on_commit=False,
    autoflush=True,
    bind=engine,
)

Base = declarative_base(metadata=metadata)


@contextmanager
def db_session() -> Generator:
    try:
        logger.debug("getting session local ... ")
        db = SessionLocal()
        logger.debug("yielding to session ... ")
        yield db
        logger.debug("committing session ... ")
        db.commit()
        logger.debug("committed session ... ")
    except Exception as e:
        logger.debug("exception raised ... ")
        logger.exception("Exception raised, rolling back changes. " f"Exception: {e}")
        logger.debug("rolling back ... ")
        db.rollback()
        logger.debug("rolled back ... ")
        logger.debug("raising exception ... ")
        raise e
    finally:
        logger.debug("closing ... ")
        db.close()
        logger.debug("closed ... ")
