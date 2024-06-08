from asyncio import current_task
from typing import AsyncGenerator, Type

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import text

from .. import DATABASE_URI, SQLALCHEMY_ECHO, SQLALCHEMY_ISOLATION_LEVEL
from .base import has_reinitialize

AsyncSQLiteEngine = create_async_engine(
    DATABASE_URI,
    echo=SQLALCHEMY_ECHO,
    isolation_level=SQLALCHEMY_ISOLATION_LEVEL,
)
AsyncSQLiteScopedSession = async_scoped_session(
    async_sessionmaker(
        AsyncSQLiteEngine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    ),
    scopefunc=current_task,
)


@event.listens_for(AsyncSQLiteEngine.sync_engine, 'connect')
def connect(dbapi_conn, connection_record):
    dbapi_conn.execute('PRAGMA foreign_keys = ON;')


async def initialize_sqlite_db(
    declarative_base: Type[DeclarativeBase],
):
    async_engine = AsyncSQLiteEngine
    metadata = declarative_base.metadata

    async with async_engine.begin() as connection:
        # enable foreign keys for SQLite
        await connection.execute(text('PRAGMA foreign_keys = ON;'))

        # drop tables if "reinitialize" flag is True
        if has_reinitialize(DATABASE_URI):
            await connection.run_sync(metadata.drop_all)

        # create tables
        await connection.run_sync(metadata.create_all)

    if (
        f'{async_engine.url.get_backend_name()}:///{async_engine.url.database}'
        != 'sqlite:///:memory:'
    ):
        await async_engine.dispose()


def get_async_sqlite_session() -> AsyncSession:
    return AsyncSQLiteScopedSession()


async def async_sqlite_session_context_manager() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSQLiteScopedSession() as session:
        yield session
