#!/usr/bin/env bats

run_database_test() {
  export DATABASE_URI=$1
  run pytest $2

  if [ $status -ne 0 ]; then
    echo "Test failed with status $status. Output: $output"
  fi

  [ $status -eq 0 ]
}

@test "Test using in-memory SQLite" {
  run_database_test "sqlite+aiosqlite:///:memory:"
}

@test "Test using MySQL" {
  run_database_test "mysql+asyncmy://user:pass@localhost:3306/test?reinitialize=true"
}

@test "Test using PostgreSQL" {
  run_database_test "postgresql+asyncpg://user:pass@localhost:5432/test?reinitialize=true"
}

@test "Test using MongoDB" {
  run_database_test "mongodb://localhost:27017/test?reinitialize=true"
}

@test "Test using Redis" {
  run_database_test "redis://:@localhost:6379/1?reinitialize=true"
}
