from typing import Any
from urllib.parse import urlparse

from settings import DATABASE_URI

IS_RELATIONAL_DB = False
IS_NOSQL = False

DATABASE_TYPE, _, _ = urlparse(DATABASE_URI).scheme.partition('+')
if DATABASE_TYPE == 'sqlite':
    from .sqlite import AsyncSQLiteEngine as AsyncRelationalDBEngine
    from .sqlite import AsyncSQLiteScopedSession as AsyncScopedSession
    from .sqlite import initialize_sqlite_db as initialize_db

    IS_RELATIONAL_DB = True
elif DATABASE_TYPE == 'mysql':
    from .mysql import AsyncMySQLEngine as AsyncRelationalDBEngine
    from .mysql import AsyncMySQLScopedSession as AsyncScopedSession
    from .mysql import initialize_mysql_db as initialize_db

    IS_RELATIONAL_DB = True
elif DATABASE_TYPE == 'postgresql':
    from .postgres import AsyncPostgreSQLEngine as AsyncRelationalDBEngine
    from .postgres import AsyncPostgreSQLScopedSession as AsyncScopedSession
    from .postgres import initialize_postgres_db as initialize_db

    IS_RELATIONAL_DB = True
elif DATABASE_TYPE == 'mongodb':
    from .mongodb import COLLECTION_NAME, DATABASE_NAME, AsyncMongoDBEngine
    from .mongodb import initialize_mongo_db as initialize_db

    IS_NOSQL = True
else:
    raise RuntimeError(
        f'Invalid database type \'{DATABASE_TYPE}\' provided in DATABASE_URI: {DATABASE_URI}'
    )
