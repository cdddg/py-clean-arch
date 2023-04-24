from sqlalchemy.engine import make_url

from settings import SQLALCHEMY_DATABASE_URI

DATABASE_BACKEND = make_url(SQLALCHEMY_DATABASE_URI).get_backend_name()
if DATABASE_BACKEND == 'sqlite':
    from .sqlite import AsyncSQLiteEngine as AsyncEngine
    from .sqlite import AsyncSQLiteScopedSession as AsyncScopedSession
    from .sqlite import initialize_sqlite_db as initialize_db
elif DATABASE_BACKEND == 'mysql':
    from .base import initialize_db
    from .mysql import AsyncMySQLEngine as AsyncEngine
    from .mysql import AsyncMySQLScopedSession as AsyncScopedSession
elif DATABASE_BACKEND == 'postgresql':
    from .base import initialize_db
    from .postgres import AsyncPostgreSQLEngine as AsyncEngine
    from .postgres import AsyncPostgreSQLScopedSession as AsyncScopedSession
else:
    raise ValueError('Invalid database backend')
