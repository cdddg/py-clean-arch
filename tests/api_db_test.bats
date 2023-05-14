#!/usr/bin/env bats

@test "Test using in-memory SQLite database" {
  export DATABASE_URL=sqlite:///:memory:
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using SQLite database" {
  export DATABASE_URL=sqlite:////tmp/test.db
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using MySQL database" {
  export DATABASE_URL=mysql://user:pass@localhost/test
  run pytest $2
  [ $status -eq 0 ]
}

@test "Test using Postgres database" {
  export DATABASE_URL=postgresql://user:pass@localhost/test
  run pytest $2
  [ $status -eq 0 ]
}

