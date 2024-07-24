<%!
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import logging
import sys
import os

Base = declarative_base()
metadata = Base.metadata

# Logging setup
logging.basicConfig()
logger = logging.getLogger('alembic.runtime.migration')

def run_migrations_offline():
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    config = context.config
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=metadata,
    )
    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
%>
