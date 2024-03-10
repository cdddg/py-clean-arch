import os

# application name and version
APP_NAME = 'Pokédex API'
APP_VERSION = '3'

# enable/disable logging of SQL statements
SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', '').lower() == 'true'

# set the isolation level for the database connection
SQLALCHEMY_ISOLATION_LEVEL = os.environ.get('SQLALCHEMY_ISOLATION_LEVEL') or 'SERIALIZABLE'

# database connection string, e.g.:
# - sqlite+aiosqlite:///sqlite.db (SQLite3)
# - sqlite+aiosqlite:///:memory: (SQLite3 in-memory)
# - mysql+asyncmy://<username>:<password>@<host>:<port>/<dbname> (MySQL)
# - postgresql+asyncpg://<username>:<password>@<host>:<port>/<dbname> (PostgreSQL)
# - mongodb://<username>:<password>@<host>:<port>/<dbname> (MongoDB)
#
# if "reinitialize" query parameter is set to "true", existing tables will be dropped before
# creating new tables. Example:
#   sqlite+aiosqlite:///sqlite.db?reinitialize=true

DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite+aiosqlite:///:memory:')
