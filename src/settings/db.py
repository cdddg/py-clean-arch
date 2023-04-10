"""
FIXME:
    To be revised to support PostgreSQL schema setting
"""

from asyncio import current_task
from logging import getLogger

from sqlalchemy.engine.url import make_url
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
    drop_existed_tables: bool = False,
):
    async with async_engine.begin() as connection:
        logger = getLogger('uvicorn.error')
        logger.info('(initialize_db) Creating db Tables...')

        if make_url(async_engine.url).get_backend_name() == 'sqlite':
            await connection.execute(text('PRAGMA foreign_keys = ON;'))

        if drop_existed_tables:
            logger.info('(initialize_db) Droping existed tables')
            await connection.run_sync(declarative_meta.metadata.drop_all)
        for k in declarative_meta.metadata.tables.keys():
            logger.info(f'(initialize_db)   - {k}')
        await connection.run_sync(declarative_meta.metadata.create_all)

    await async_engine.dispose()
