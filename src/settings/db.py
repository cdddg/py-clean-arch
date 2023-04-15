"""
FIXME:
    To be revised to support PostgreSQL schema setting
"""

from asyncio import current_task
from logging import Logger, getLogger

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql import text

from . import IS_TEST, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ECHO
from .test import pytest_scope_func

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=SQLALCHEMY_ECHO,
    isolation_level='SERIALIZABLE',
)


AsyncScopedSession = async_scoped_session(
    sessionmaker(
        async_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    ),
    scopefunc=current_task if not IS_TEST else pytest_scope_func,
)


def get_async_engine() -> AsyncEngine:
    return async_engine


# pylint: disable=no-member,redefined-outer-name
async def initialize_db(
    declarative_meta: DeclarativeMeta,
    async_engine: AsyncEngine,
    logger: Logger = getLogger('uvicorn.error'),
):
    logger.info('(initialize_db) Creating database tables...')

    # enable foreign keys for SQLite
    if async_engine.url.get_backend_name() == 'sqlite':
        async with async_engine.begin() as connection:
            await connection.execute(text('PRAGMA foreign_keys = ON;'))

    metadata = declarative_meta.metadata

    # drop tables if "drop_existed" flag is True
    if async_engine.url.query.get('drop_existed', '').lower() == 'true':
        logger.info('(initialize_db) Dropping existing tables')
        async with async_engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)

    # create tables
    for table_name in metadata.tables.keys():
        logger.info(f'(initialize_db)   - {table_name}')
    async with async_engine.begin() as connection:
        await connection.run_sync(metadata.create_all)

    # dispose engine if not using in-memory database
    if (
        f'{async_engine.url.get_backend_name()}:///{async_engine.url.database}'
        != 'sqlite:///:memory:'
    ):
        await async_engine.dispose()
