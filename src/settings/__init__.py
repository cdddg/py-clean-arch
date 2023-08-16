import os

# Application name and version
APP_NAME = 'Pokédex API'
APP_VERSION = '3'

# Check if running in a test environment
IS_TEST = os.getenv('TEST', '').lower() == 'true'

# Enable/disable logging of SQL statements
SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', '').lower() == 'true'

# Database connection string, e.g.:
# - sqlite+aiosqlite:///sqlite.db (SQLite3)
# - sqlite+aiosqlite://:memory: (SQLite3 in-memory)
# - mysql+asyncmy://<username>:<password>@<host>:<port>/<dbname> (MySQL)
# - postgresql+asyncpg://<username>:<password>@<host>:<port>/<dbname> (PostgreSQL)
#
# If `drop_existed` query parameter is set to `true`, existing tables will be dropped before
# creating new tables. Example:
#   sqlite+aiosqlite:///sqlite.db?drop_existed=true
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite+aiosqlite:///sqlite.db')

# Set the isolation level for the database connection
SQLALCHEMY_ISOLATION_LEVEL = 'SERIALIZABLE'
