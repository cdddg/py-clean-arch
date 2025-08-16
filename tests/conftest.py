import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient
from pytest import Config

from main import app as fastapi_app
from settings.db import IS_DOCUMENT_DB, IS_KEY_VALUE_DB, IS_RELATIONAL_DB, initialize_db


def pytest_configure(config: Config):
    echo = print  # ignore: remove-print-statements
    echo(__file__)
    echo(f'DATABASE_URI={os.environ["DATABASE_URI"]}')


def deep_compare(d1, d2, ignore_marker='...'):
    """
    Recursively compares two dictionaries or lists, ignoring specific values marked by an ignore marker.

    This function can be particularly useful in testing scenarios where some data fields (e.g., IDs or timestamps)
    may not be predictable and should be ignored for comparison purposes.

    Args:
        d1 (dict | list): The first dictionary or list to compare.
        d2 (dict | list): The second dictionary or list to compare.
        ignore_marker (str): The marker that indicates a value should be ignored in comparison. Defaults to '...'.

    Returns:
        bool: True if d1 and d2 are considered equal when ignoring specified markers; False otherwise.

    Examples:
        >>> expected = {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '...', 'name': 'Grass'},
                {'id': '...', 'name': 'Poison'}
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        }
        >>> actual = {
            'no': '0001',
            'name': 'Bulbasaur',
            'types': [
                {'id': '3190ea067bad44679924a550498317c1', 'name': 'Grass'},
                {'id': '26a1369b28524699a13036ccfb33a261', 'name': 'Poison'}
            ],
            'previous_evolutions': [],
            'next_evolutions': [],
        }
        >>> deep_compare(expected, actual)
        True
    """
    if isinstance(d1, dict) and isinstance(d2, dict):  # pylint: disable=no-else-return
        if d1.keys() != d2.keys():
            return False
        return all(deep_compare(d1[key], d2[key], ignore_marker) for key in d1)
    elif isinstance(d1, list) and isinstance(d2, list):
        if len(d1) != len(d2):
            return False
        return all(deep_compare(item1, item2, ignore_marker) for item1, item2 in zip(d1, d2))
    else:
        return d1 == d2 or d1 == ignore_marker or d2 == ignore_marker


@pytest.fixture(scope='session')
def anyio_backend():
    yield 'asyncio'


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(base_url='http://test', transport=ASGITransport(app=fastapi_app)) as ac:
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
        await initialize_db(declarative_base=Base)  # pyright: ignore[reportCallIssue]

    @pytest.fixture(scope='function', autouse=True)
    async def session():
        # ref:
        #   https://stackoverflow.com/questions/65528675
        #   https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
        async with AsyncRelationalDBEngine.connect() as conn:
            # XXX: SQLite connection issue - await conn.begin() doesn't work as expected
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

            # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.async_scoped_session.remove
            await AsyncScopedSession.remove()

    @pytest.fixture(scope='function', autouse=True)
    def patch_functions(session):  # pylint: disable=redefined-outer-name
        with (
            patch('settings.db.get_async_session', return_value=session),
            patch('di.unit_of_work.AsyncSQLAlchemyUnitOfWork.remove', new_callable=AsyncMock),
        ):
            yield

elif IS_DOCUMENT_DB or IS_KEY_VALUE_DB:

    @pytest.fixture(scope='function', autouse=True)
    async def engine():
        await initialize_db()
