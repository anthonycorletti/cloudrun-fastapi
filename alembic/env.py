import os
import re
import time
from logging import basicConfig

from alembic import context
from sqlalchemy import create_engine

from config import apisecrets
from database import Base
from models.item import Item  # noqa
from models.user import User  # noqa

# configure local env setup
os.environ['TZ'] = 'UTC'
tz = time.strftime('%z')

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
basicConfig(format=(f'[%(asctime)s.%(msecs)03d {tz}] '
                    '[%(process)s] [%(filename)s L%(lineno)d] '
                    '[%(levelname)s] %(message)s'),
            level='INFO',
            datefmt='%Y-%m-%d %H:%M:%S')

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    url = None
    project_id = os.getenv('PROJECT_ID')

    if project_id:
        url = re.sub('/cloudsql/', '/tmp/cloudsql/', apisecrets.DATABASE_URL)
    else:
        url = apisecrets.DATABASE_URL

    if not url:
        raise ValueError(
            f'given project id: {project_id}, database url is not set')

    return url


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_url(), pool_pre_ping=True)

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
