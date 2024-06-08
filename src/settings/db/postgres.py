from asyncio import current_task
from typing import AsyncGenerator, Type

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .. import DATABASE_URI, SQLALCHEMY_ECHO, SQLALCHEMY_ISOLATION_LEVEL
from .base import has_reinitialize, normalize_uri

# pylint: disable=duplicate-code
# Disabling due to similar implementation in postgres.py and mysql.py, leading to code duplication.


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
    scopefunc=current_task,
)


async def initialize_postgres_db(declarative_base: Type[DeclarativeBase]):
    async_engine = AsyncPostgreSQLEngine
    metadata = declarative_base.metadata

    async with async_engine.begin() as connection:
        # drop tables if "reinitialize" flag is True
        if has_reinitialize(DATABASE_URI):
            await connection.run_sync(metadata.drop_all)

        # create tables
        await connection.run_sync(metadata.create_all)

    await async_engine.dispose()


def get_async_postgresql_session() -> AsyncSession:
    return AsyncPostgreSQLScopedSession()


async def async_postgresql_session_context_manager() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncPostgreSQLScopedSession() as session:
        yield session
