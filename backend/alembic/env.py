from logging.config import fileConfig
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool

from alembic import context

from app.models import User, AuthProvider
from app.core.database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
from app.core.config import DB_URL

config.set_main_option(
    "sqlalchemy.url",
    DB_URL
)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    
    # 1. Create the async engine from config sections
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # 2. Define the async execution wrapper
    async def do_run_migrations():
        async with connectable.connect() as connection:
            # Passes a synchronous proxy connection to Alembic's sync engine
            await connection.run_sync(do_meta_migrations)

    # 3. Define the synchronous runner configuration
    def do_meta_migrations(sync_conn):
        context.configure(
            connection=sync_conn, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

    # 4. Trigger the event loop to orchestrate the blocks
    asyncio.run(do_run_migrations())



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
