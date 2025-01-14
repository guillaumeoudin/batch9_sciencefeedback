from __future__ import with_statement
import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine


APP_NAME = os.environ.get('APP_NAME')
COMPOSITION = os.environ.get('COMPOSITION')
LOCALHOST_POSTGRES_URL = f'postgresql://{APP_NAME}_user:{APP_NAME}_password@apipostgresdb-{COMPOSITION}/{APP_NAME}_apipostgres'
POSTGRES_URL = os.environ.get('POSTGRES_URL', LOCALHOST_POSTGRES_URL)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# SPECIAL CONFIG REMOVE TRANSITION and GET URL FROM DATABASE URL
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in ('alembic_version', 'transaction', 'activity'):
        return False
    else:
        return True

def get_url():
    return POSTGRES_URL

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
    context.configure(url=url,
                      include_object=include_object,
                      include_schemas=True,
                      literal_binds=True,
                      target_metadata=target_metadata,)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(get_url())


    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            include_object=include_object,
            include_schemas=True,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
