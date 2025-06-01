#!/usr/bin/env bats

setup() {
  : "${SQLITE_URL:=sqlite+aiosqlite:///:memory:}"
  : "${MYSQL_URL:=mysql+asyncmy://user:pass@localhost:3306/test_db?reinitialize=true}"
  : "${POSTGRES_URL:=postgresql+asyncpg://user:pass@localhost:5432/test_db?reinitialize=true}"
  : "${MONGO_URL:=mongodb://localhost:27017/test_db?reinitialize=true}"
  : "${REDIS_URL:=redis://:@localhost:6379/15?reinitialize=true}"
}

run_database_test() {
  local db_uri=$1
  local extra_args=$2

  export DATABASE_URI="$db_uri"
  run pytest $extra_args

  if [ $status -ne 0 ]; then
    echo "Test failed with status $status. Output: $output"
  fi

  [ $status -eq 0 ]
}

@test "Test using in-memory SQLite" {
  run_database_test "$SQLITE_URL"
}

@test "Test using MySQL" {
  run_database_test "$MYSQL_URL"
}

@test "Test using PostgreSQL" {
  run_database_test "$POSTGRES_URL"
}

@test "Test using MongoDB" {
  run_database_test "$MONGO_URL"
}

@test "Test using Redis" {
  run_database_test "$REDIS_URL"
}
