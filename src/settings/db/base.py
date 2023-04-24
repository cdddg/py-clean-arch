from logging import Logger, getLogger

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine as SQLAlchemyAsyncEngine
from sqlalchemy.orm.decl_api import DeclarativeMeta

from .. import SQLALCHEMY_DATABASE_URI


def get_parsed_database_uri(uri) -> str:
    uri = make_url(uri)
    query_dict = dict(uri.query)
    query_dict.pop('drop_existed', None)
    new_query_str = '&'.join(f'{k}={v}' for k, v in query_dict.items())

    return f'{uri.drivername}://{uri.username}:{uri.password}@{uri.host}/{uri.database}?{new_query_str}'


def is_drop_existed(uri) -> bool:
    uri = make_url(uri)

    return str(uri.query.get('drop_existed')).lower() == 'true'


async def initialize_db(
    declarative_meta: DeclarativeMeta,
    async_engine: SQLAlchemyAsyncEngine,
    logger: Logger = getLogger('uvicorn.error'),
):
    metadata = declarative_meta.metadata

    logger.info('(initialize_db) Creating database tables...')
    async with async_engine.begin() as connection:
        # drop tables if "drop_existed" flag is True
        if is_drop_existed(SQLALCHEMY_DATABASE_URI):
            logger.info('(initialize_db) Dropping existing tables')
            await connection.run_sync(metadata.drop_all)

        # create tables
        for table_name in metadata.tables.keys():
            logger.info(f'(initialize_db)   - {table_name}')
        await connection.run_sync(metadata.create_all)

    await async_engine.dispose()
