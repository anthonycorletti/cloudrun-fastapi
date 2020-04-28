import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

from config import apisecrets

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=NAMING_CONVENTION)

SQLALCHEMY_DATABASE_URL = apisecrets.DATABASE_URL
logger = logging.getLogger(__name__)

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_pre_ping=True,
                       pool_size=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base(metadata=metadata)


def get_db():
    try:
        db = SessionLocal()
        yield db
        db.commit()
    except Exception as e:
        logger.error(('Exception raised, rolling back changes. '
                      f'Exception: {e}'))
        db.rollback()
        raise e
    finally:
        db.close()
