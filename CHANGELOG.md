# Changelog

- **v1**: Check out the [v1 branch](https://github.com/cdddg/py-clean-arch/tree/v1).<br> Archived in April 2021. <br>
  Description: Initial proposal by me.

  > Core Architecture Setup<br>
  > ☑️ Built complete `FastAPI` project structure with modular `src/` organization<br>
  > ☑️ Implemented `Repository pattern` for data access layer
  >
  > API Implementation<br>
  > ☑️ Implemented `RESTful` Pokemon `CRUD` endpoints<br>
  >
  > Development Tooling<br>
  > ☑️ Added `Docker` containerization support<br>
  > ☑️ Established `pytest` testing framework with test cases

- **v2**: Check out the [v2 branch](https://github.com/cdddg/py-clean-arch/tree/v2).<br> Archived in July 2023. <br>
  Description: Improvement from v1, For details, see [PR #1 to PR #10](https://github.com/cdddg/py-clean-arch/pulls?q=is%3Apr+is%3Aclosed+merged%3A2023-04-09..2023-08-15)

  > Core Refactor: Inspired by [go-clean-arch v3](https://github.com/bxcodec/go-clean-arch/tree/v3)<br>
  > ☑️ Adopted Go project directory structure: `pkg/deliveries/`, `pkg/repositories/`, `pkg/usecases/`
  >
  > Clean Architecture Implementation<br>
  > ☑️ Added `Unit of Work` and `Dependency Injection` design patterns<br>
  > ☑️ Strict separation of layer responsibilities following Uncle Bob's `Clean Architecture` principles
  >
  > API Style Expansion<br>
  > ☑️ Added comprehensive `GraphQL` API support (mutations, queries, schemas)
  >
  > Multi-Database Support<br>
  > ☑️ Multi-database support: `MySQL`, `PostgreSQL`, `SQLite`<br>
  > ☑️ Implemented async `SQLAlchemy 2.0`

- **v3**: Check out the [v3 branch](https://github.com/cdddg/py-clean-arch/tree/v3). <br> Archived in August 2025. <br>Description: Transition to Python-centric design from Go. For details, see [PR #11 to PR #46](https://github.com/cdddg/py-clean-arch/pulls?q=is%3Apr+is%3Aclosed+merged%3A2023-08-15..2025-08-02).

  > Go-style to Python-centric Transition<br>
  > ☑️ Removed Go-idiomatic `pkg/` structure, adopted Python ecosystem conventions
  >
  > NoSQL Database Expansion<br>
  > ☑️ Added `MongoDB` document database support (`document-oriented`)<br>
  > ☑️ Added `Redis` key-value database support (`key-value store`)
  >
  > Testing Architecture Enhancement<br>
  > ☑️ Established three-tier testing structure: `unit`, `integration`, `functional`
  >
  > DevOps and Toolchain<br>
  > ☑️ Added `GitHub Actions` CI/CD pipeline<br>
  > ☑️ Integrated code quality tools: `cspell`, `pylint`, `ruff`, `pyright`

- ✏️ **v4**: Currently making minor refinements on the [master](https://github.com/cdddg/py-clean-arch/tree/master) branch. The scope for the next major iteration has not been decided yet.

  > Toolchain Migration<br>
  > ☑️ Migrated package manager from `Poetry` to `uv`
