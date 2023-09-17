#!/usr/bin/env bats

@test "Test using SQLite database" {
  export DATABASE_URI=sqlite+aiosqlite:///test.db?reinitialize=true;
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using in-memory SQLite database" {
  export DATABASE_URI=sqlite+aiosqlite:///:memory:
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using MySQL database" {
  export DATABASE_URI=mysql+asyncmy://user:pass@localhost:3306/test?reinitialize=true
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using Postgres database" {
  export DATABASE_URI=postgresql+asyncpg://user:pass@localhost:5432/test?reinitialize=true
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using MongoDB database" {
  export DATABASE_URI=mongodb://localhost:27017/test?reinitialize=true
  run pytest $2
  [ $status -eq 0 ]
}
