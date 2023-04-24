from asyncio import current_task
from logging import Logger, getLogger

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine as SQLAlchemyAsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql import text

from .. import IS_TEST, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ECHO, SQLALCHEMY_ISOLATION_LEVEL
from ..test import pytest_scope_func
from .base import is_drop_existed


async def initialize_sqlite_db(
    declarative_meta: DeclarativeMeta,
    async_engine: SQLAlchemyAsyncEngine,
    logger: Logger = getLogger('uvicorn.error'),
):
    metadata = declarative_meta.metadata

    logger.info('(initialize_db) Creating database tables...')
    async with async_engine.begin() as connection:
        # enable foreign keys for SQLite
        await connection.execute(text('PRAGMA foreign_keys = ON;'))

        # drop tables if "drop_existed" flag is True
        if is_drop_existed(SQLALCHEMY_DATABASE_URI):
            logger.info('(initialize_db) Dropping existing tables')
            await connection.run_sync(metadata.drop_all)

        # create tables
        for table_name in metadata.tables.keys():
            logger.info(f'(initialize_db)   - {table_name}')
        await connection.run_sync(metadata.create_all)

    if (
        f'{async_engine.url.get_backend_name()}:///{async_engine.url.database}'
        != 'sqlite:///:memory:'
    ):
        await async_engine.dispose()


AsyncSQLiteEngine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=SQLALCHEMY_ECHO,
    isolation_level=SQLALCHEMY_ISOLATION_LEVEL,
)


@event.listens_for(AsyncSQLiteEngine.sync_engine, 'connect')
def connect(dbapi_conn, connection_record):
    dbapi_conn.execute('PRAGMA foreign_keys = ON;')


AsyncSQLiteScopedSession = async_scoped_session(
    sessionmaker(
        AsyncSQLiteEngine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    ),
    scopefunc=current_task if not IS_TEST else pytest_scope_func,
)
