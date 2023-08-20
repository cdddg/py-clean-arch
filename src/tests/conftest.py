import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient
from pytest import Config
from sqlalchemy import event
from sqlalchemy.sql import text

from app.di.unit_of_work import AsyncSqlAlchemyUnitOfWork
from app.repositories.rdbms.pokemon.orm import Base
from main import app as fastapi_app
from settings.db import AsyncEngine, AsyncScopedSession, initialize_db


def pytest_configure(config: Config):
    echo = print  # ignore: remove-print-statements
    echo(__file__)
    echo(f'SQLALCHEMY_DATABASE_URI={os.environ["SQLALCHEMY_DATABASE_URI"]}')


@pytest.fixture(scope='session')
def anyio_backend():
    yield 'asyncio'


@pytest.fixture(scope='session', autouse=True)
async def engine():
    await initialize_db(Base, AsyncEngine)

    yield AsyncEngine


@pytest.fixture(scope='module')
async def client():
    """
    Asynchronous fixture to create an AsyncClient instance for testing FastAPI routes.

    This fixture initiates an event loop that's required for the asynchronous
    operations in the tests. When AsyncClient is used along with a FastAPI application,
    it might start or affect the event loop in some way. This means that any test
    which uses this fixture will have an active event loop, ready for asynchronous
    operations.

    It's essential to ensure that there's an active event loop when performing
    async operations. If not, tests might throw errors indicating that the event
    loop is closed or not available. This is why importing and using this fixture
    helped resolve the error in some tests, ensuring they had the necessary setup
    for async operations.
    """

    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='function', autouse=True)
async def session():
    # ref:
    #   https://stackoverflow.com/questions/65528675
    #   https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async with AsyncEngine.connect() as conn:
        # TODO: Not sure why `await conn.begin()` doesn't work when DB is sqlite
        await conn.execute(text('BEGIN'))
        await conn.begin_nested()

        async_session = AsyncScopedSession(bind=conn)

        @event.listens_for(async_session.sync_session, 'after_transaction_end')
        def end_savepoint(sess, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()  # pyright: ignore[reportOptionalMemberAccess]

        yield async_session


@pytest.fixture(scope='function')
async def mock_async_uow():
    auow = MagicMock(spec=AsyncSqlAlchemyUnitOfWork)
    auow.__aenter__.return_value = auow
    auow.pokemon_repo = AsyncMock()
    auow.type_repo = AsyncMock()
    auow.evolution_repo = AsyncMock()

    with patch('app.usecases.pokemon.async_unit_of_work', return_value=auow):
        yield auow
