import pytest
from httpx import AsyncClient
from pytest import Config
from sqlalchemy import event
from sqlalchemy.sql import text
import os

from main import app
from pkg.repositories.rdbms.pokemon.orm import DeclarativeMeta
from settings.db import AsyncEngine, AsyncScopedSession, initialize_db


def pytest_configure(config: Config):
    print(os.environ['SQLALCHEMY_DATABASE_URI'])

@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session', autouse=True)
async def engine():
    await initialize_db(DeclarativeMeta, AsyncEngine)

    return AsyncEngine


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='function', autouse=True)
async def session():
    # ref:
    #   https://stackoverflow.com/questions/65528675
    #   https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async with AsyncEngine.connect() as conn:
        await conn.execute(
            text('BEGIN')
        )  # Not sure why `await conn.begin()` doesn't work when DB is sqlite
        await conn.begin_nested()

        async_session = AsyncScopedSession(bind=conn)

        @event.listens_for(async_session.sync_session, 'after_transaction_end')
        def end_savepoint(sess, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()  # type: ignore[reportOptionalMemberAccess]

        yield async_session
