"""
FIXME: known bug
  1. `sqlite+aiosqlite:///:memory:` not working (sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: pokemon)
  2. `sqlite+aiosqlite:///./src/tests/test.db` savepoint not working
"""
