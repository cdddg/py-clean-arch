#!/usr/bin/env bats

@test "Test using SQLite database" {
  export SQLALCHEMY_DATABASE_URI=sqlite+aiosqlite:///test.db?drop_existed=true;
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using in-memory SQLite database" {
  export SQLALCHEMY_DATABASE_URI=sqlite+aiosqlite:///:memory:
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using MySQL database" {
  export SQLALCHEMY_DATABASE_URI=mysql+asyncmy://user:pass@localhost:3306/test?drop_existed=true
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using Postgres database" {
  export SQLALCHEMY_DATABASE_URI=postgresql+asyncpg://user:pass@localhost:5432/test?drop_existed=true
  run pytest $2
  [ $status -eq 0 ]
}

