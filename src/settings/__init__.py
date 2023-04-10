import os

APP_NAME = 'Pokédex API'
APP_VERSION = '2'

IS_TEST = os.getenv('TEST', '').lower() == 'true'
SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', '').lower() == 'true'
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite+aiosqlite:///sqlite.db')
# e.x.:
#   - sqlite+aiosqlite:///sqlite.db
#   - sqlite+aiosqlite://:memory:
#   - mysql+asyncmy://<username>:<password>@<host>:<port>/<dbname>
#   - postgresql+asyncpg://<username>:<password>@<host>:<port>/<dbname>
