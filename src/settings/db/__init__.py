from urllib.parse import urlparse

from settings import DATABASE_URI

IS_RELATIONAL_DB = False
IS_DOCUMENT_DB = False
IS_KEY_VALUE_DB = False

DATABASE_TYPE, _, _ = urlparse(DATABASE_URI).scheme.partition('+')
if DATABASE_TYPE == 'sqlite':
    from .sqlite import AsyncSQLiteEngine as AsyncRelationalDBEngine
    from .sqlite import AsyncSQLiteScopedSession as AsyncScopedSession
    from .sqlite import get_async_sqlite_session as get_async_session
    from .sqlite import initialize_sqlite_db as initialize_db

    IS_RELATIONAL_DB = True

elif DATABASE_TYPE == 'mysql':
    from .mysql import AsyncMySQLEngine as AsyncRelationalDBEngine
    from .mysql import AsyncMySQLScopedSession as AsyncScopedSession
    from .mysql import get_async_mysql_session as get_async_session
    from .mysql import initialize_mysql_db as initialize_db

    IS_RELATIONAL_DB = True

elif DATABASE_TYPE == 'postgresql':
    from .postgres import AsyncPostgreSQLEngine as AsyncRelationalDBEngine
    from .postgres import AsyncPostgreSQLScopedSession as AsyncScopedSession
    from .postgres import get_async_postgresql_session as get_async_session
    from .postgres import initialize_postgres_db as initialize_db

    IS_RELATIONAL_DB = True

elif DATABASE_TYPE == 'mongodb':
    from .mongodb import COLLECTION_NAME, DATABASE_NAME, AsyncMongoDBEngine
    from .mongodb import initialize_mongo_db as initialize_db

    IS_DOCUMENT_DB = True

elif DATABASE_TYPE == 'redis':
    from .redis import get_async_redis_client as get_async_client
    from .redis import initialize_redis as initialize_db

    IS_KEY_VALUE_DB = True

else:
    raise RuntimeError(
        f'Invalid database type \'{DATABASE_TYPE}\' provided in DATABASE_URI: {DATABASE_URI}'
    )
