import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient
from pytest import Config

from main import app as fastapi_app
from settings.db import IS_NOSQL, IS_RELATIONAL_DB, initialize_db


def pytest_configure(config: Config):
    echo = print  # ignore: remove-print-statements
    echo(__file__)
    echo(f'DATABASE_URI={os.environ["DATABASE_URI"]}')


@pytest.fixture(scope='session')
def anyio_backend():
    yield 'asyncio'


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
async def mock_async_unit_of_work():
    auow = MagicMock()
    auow.__aenter__.return_value = auow
    auow.pokemon_repo = AsyncMock()

    yield auow


if IS_RELATIONAL_DB:
    # pylint: disable=ungrouped-imports
    from sqlalchemy import event
    from sqlalchemy.sql import text

    from repositories.relational_db.pokemon.orm import Base
    from settings.db import AsyncRelationalDBEngine, AsyncScopedSession

    @pytest.fixture(scope='package', autouse=True)
    async def engine():
        await initialize_db(declarative_base=Base)

    @pytest.fixture(scope='function', autouse=True)
    async def session():
        # ref:
        #   https://stackoverflow.com/questions/65528675
        #   https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
        async with AsyncRelationalDBEngine.connect() as conn:
            # TODO: Not sure why `await conn.begin()` doesn't work when DB is sqlite
            await conn.execute(text('BEGIN'))
            await conn.begin_nested()

            async_session = AsyncScopedSession(bind=conn)

            @event.listens_for(async_session.sync_session, 'after_transaction_end')
            def end_savepoint(*args, **kwargs):
                if conn.closed:
                    return
                if not conn.in_nested_transaction():
                    conn.sync_connection.begin_nested()  # pyright: ignore[reportOptionalMemberAccess]

            yield async_session

    @pytest.fixture(scope='function', autouse=True)
    def patch_functions(session):  # pylint: disable=redefined-outer-name
        with (
            patch('settings.db.get_async_session', return_value=session),
            patch('di.unit_of_work.AsyncSQLAlchemyUnitOfWork.remove', new_callable=AsyncMock),
        ):
            yield

elif IS_NOSQL:

    @pytest.fixture(scope='function', autouse=True)
    async def engine():
        await initialize_db()
