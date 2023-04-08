import pytest
from httpx import AsyncClient
from sqlalchemy import event

from main import app
from pkg.repositories.rdbms.pokemon.orm import DeclarativeMeta
from settings.db import AsyncScopedSession, get_async_engine, initialize_db


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='module', autouse=True)
async def engine():
    async_engine = get_async_engine()
    await initialize_db(DeclarativeMeta, async_engine)

    return async_engine


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(app=app, base_url=f'http://test') as ac:
        yield ac


@pytest.fixture(scope='function')
async def session(engine):
    # ref:
    #   https://stackoverflow.com/questions/65528675
    #   https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = engine
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        async_session = AsyncScopedSession(bind=conn)

        @event.listens_for(async_session.sync_session, 'after_transaction_end')
        def end_savepoint(sess, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()  # type: ignore[reportOptionalMemberAccess]

        yield async_session

    await async_engine.dispose()
