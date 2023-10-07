from asyncio import current_task
from logging import Logger, getLogger
from typing import Type

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .. import DATABASE_URI, IS_TESTING, SQLALCHEMY_ECHO, SQLALCHEMY_ISOLATION_LEVEL
from ..test import pytest_scope_func
from .base import normalize_uri, should_reinitialize

AsyncPostgreSQLEngine = create_async_engine(
    normalize_uri(DATABASE_URI),
    echo=SQLALCHEMY_ECHO,
    isolation_level=SQLALCHEMY_ISOLATION_LEVEL,
)

AsyncPostgreSQLScopedSession = async_scoped_session(
    async_sessionmaker(
        AsyncPostgreSQLEngine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    ),
    scopefunc=current_task if not IS_TESTING else pytest_scope_func,
)


async def initialize_postgres_db(
    declarative_base: Type[DeclarativeBase],
    logger: Logger = getLogger('uvicorn.error'),
):
    async_engine = AsyncPostgreSQLEngine
    scheme = async_engine.url.get_backend_name()
    metadata = declarative_base.metadata

    logger.info(f'(initialize_{scheme}_db) Creating database tables...')
    async with async_engine.begin() as connection:
        # drop tables if "reinitialize" flag is True
        if should_reinitialize(DATABASE_URI):
            logger.info(f'(initialize_{scheme}_db) Dropping existing tables')
            await connection.run_sync(metadata.drop_all)

        # create tables
        for table_name in metadata.tables.keys():
            logger.info(f'(initialize_{scheme}_db)   - {table_name}')
        await connection.run_sync(metadata.create_all)

    await async_engine.dispose()
