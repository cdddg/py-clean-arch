from asyncio import current_task
from logging import Logger, getLogger
from typing import Type

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
from .base import should_reinitialize

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
    logger: Logger = getLogger('uvicorn.error'),
):
    async_engine = AsyncSQLiteEngine
    metadata = declarative_base.metadata

    logger.info('(initialize_sqlite_db) Creating database tables...')
    async with async_engine.begin() as connection:
        # enable foreign keys for SQLite
        await connection.execute(text('PRAGMA foreign_keys = ON;'))

        # drop tables if "reinitialize" flag is True
        if should_reinitialize(DATABASE_URI):
            logger.info('(initialize_db) Dropping existing tables')
            await connection.run_sync(metadata.drop_all)

        # create tables
        for table_name in metadata.tables.keys():
            logger.info(f'(initialize_sqlite_db)   - {table_name}')
        await connection.run_sync(metadata.create_all)

    if (
        f'{async_engine.url.get_backend_name()}:///{async_engine.url.database}'
        != 'sqlite:///:memory:'
    ):
        await async_engine.dispose()
