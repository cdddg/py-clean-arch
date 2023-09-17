# Python Clean Architecture

This is an example of implementing a Pokémon API based on the Clean Architecture in a Python project, referencing [**go-clean-arch**](https://github.com/bxcodec/go-clean-arch)

## Changelog

- **v1**: Check out the [v1 branch](https://github.com/cdddg/py-clean-arch/tree/v1).<br> Archived to the v1 branch in April 2021. <br>**Description**: Initial proposal by me.
- **v2**: Check out the [v2 branch](https://github.com/cdddg/py-clean-arch/tree/v2).<br> Archived to the v2 branch in July 2023. <br>**Description**: Improvements from v1 spanning from [PR #1 .. PR #10](https://github.com/cdddg/py-clean-arch/pulls?q=is%3Apr+is%3Aclosed+merged%3A2023-04-09..2023-08-15+).
- **v3**: Current version on the master branch.<br> Merged to master in August 2023. <br>
  **Description**:Transition from Go-centric design to conventional Python practices, starting with PR [#11](https://github.com/cdddg/py-clean-arch/pull/11). See the full list of [PRs](https://github.com/cdddg/py-clean-arch/pulls?q=is%3Apr+is%3Aclosed+merged%3A2023-08-16..2099-12-31+) up to the present.

## Description

Core Principles of Clean Architecture by Uncle Bob: [^1]

1. **Independent of Frameworks:** The architecture does not depend on the existence of some library of feature laden software. This allows you to use such frameworks as tools, rather than having to cram your system into their limited constraints.
2. **Testable:** The business rules can be tested without the UI, Database, Web Server, or any other external element.
3. **Independent of UI:** The UI can change easily, without changing the rest of the system. A Web UI could be replaced with a console UI, for example, without changing the business rules.
4. **Independent of Database:** You can swap out Oracle or SQL Server, for Mongo, BigTable, CouchDB, or something else. Your business rules are not bound to the database.
5. **Independent of any External Agency:** In fact your business rules simply don’t know anything at all about the outside world.

![clean-arch-01](./docs/clean-arch-01.png)

![clean-arch-02](./docs/clean-arch-02.png)

### Additional Features and Patterns in This Project

This project doesn't just adhere to Uncle Bob's Clean Architecture principles; it also brings in modern adaptions and extended features to suit contemporary development needs:

- **GraphQL vs HTTP**: The `deliveries` module houses two API interfaces. `graphql` provides for a robust GraphQL API, while `http` focuses on RESTful API routes and controls.

- **RelationalDB vs NoSQL**: The `repositories` module supports both relational and NoSQL databases. `relationaldb` manages databases like SQLite, MySQL, and PostgreSQL, whereas `nosql` caters to NoSQL databases like MongoDB and CouchDB.

Apart from following Uncle Bob's Clean Architecture, this project also incorporates:

- **Unit of Work Pattern**: Ensures that all work is completed as a single unit for every transactional operation. [^2]
- **Dependency Injection Pattern**: Helps in reducing direct dependencies between codes, increasing the testability and flexibility of modules. [^3]
- **Asynchronous SQLalchemy**: By utilizing the asynchronous capabilities of SQLAlchemy 2.0, database operations are optimized for performance and efficiently handle multitasking. [^4]

### Project Structure Overview & Clean Architecture Mapping

The directory structure below provides a high-level view of the project. Each directory or module corresponds to a layer in Uncle Bob's Clean Architecture. Please note that only the main directories and key files are listed here. Some specific files or subdirectories might be omitted to highlight the overall architecture and the primary purpose of each layer.

```
src
├── app/
│   ├── deliveries/         - External interfaces like HTTP & GraphQL endpoints.
│   │   ├── graphql/        - GraphQL components for a flexible API.
│   │   └── http/           - RESTful API routes and controllers
│   │                         ('Frameworks and Drivers' in Clean Architecture)
│   │
│   ├── usecases/           - Contains application-specific business rules.
│   │                         ('Use Cases' in Clean Architecture)
│   │
│   ├── repositories/       - Data interaction layer, converting domain data to/from database format.
│   │   ├── relationaldb/   - Operations for relational databases (e.g., SQLite, MySQL, PostgreSQL).
│   │   └── nosql/          - Operations for NoSQL databases (e.g., MongoDB, CouchDB).
│   │                         ('Interface Adapters' in Clean Architecture)
│   │
│   └── di/                 - Dependency injection module.
│       ├── dependency_injection.py
│       └── unit_of_work.py
│
├── models/                 - Entity representations & core business logic.
│                             ('Entities' in Clean Architecture)
│
├── common/                 - Shared code and utilities.
│
├── settings/               - Application configurations.
│
├── tests/                  - Testing module for the application.
│   ├── unit/               - Tests for individual components in isolation.
│   └── integration/        - Tests for interactions between components.
│
└── main.py                 - Main file to launch the application.

```

## How To Run This Project

### Run the Application

```sh
$ docker-compose up
```

or

pre-work, install python (>=3.10), poetry (>=1.5.1,<1.6) and setup

```sh
$ poetry env use python
$ poetry shell
$ poetry install --no-root
```

```sh
$ make up
```

application run on http://localhost:8000

![fastapi-doc](./docs/fastapi-doc.png)

### Run the Testing

To test a single database, set the `DATABASE_URI` environment variable to the database URI and run:

```sh
$ DATABASE_URI=<database-uri> pytest
```

> Note: By default, an in-memory SQLite database is used if no URI is provided.
>

\---

Test multiple databases (in-memory SQLite, SQLite, MySQL, Postgres):

###### Install bats

To test multiple databases, you need to install the `bats` testing framework. On macOS, you can use [Homebrew](https://brew.sh/) to install `bats`:

```sh
$ brew install bats
```

On Linux, you can download `bats` from the official [GitHub repository](https://github.com/bats-core/bats-core) and compile it:

```sh
$ git clone https://github.com/bats-core/bats-core.git
$ cd bats-core
$ ./install.sh /usr/local
```

###### Run the tests

Once you have installed `bats`, run the following commands to test multiple databases:

1. Set up the databases:

   ```sh
   $ make db
   ```

2. Run the tests:

   ```sh
   $ make test
   ```

3. Here are the typical test results when using different databases:

   ```sh
     api_db_test.bats
      ✓ Test using SQLite database [10878ms]
      ✓ Test using in-memory SQLite database [3708ms]
      ✓ Test using MySQL database [5518ms]
      ✓ Test using Postgres database [4582ms]
      ✓ Test using MongoDB database [4606ms]
   
     5 tests, 0 failures in 30 seconds
   ```


### Code Coverage

As part of our commitment to maintain high standards, we use `pytest-cov` to ensure extensive test coverage. Currently, our code coverage stands at 91.33%. [^5]

To generate a coverage report:

```sh
$ pytest --cov
```



[^1]: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
[^2]: https://www.cosmicpython.com/book/chapter_06_uow.html
[^3]: https://en.wikipedia.org/wiki/Dependency_injection
[^4]:  The asyncio extension as of SQLAlchemy 1.4.3 can now be considered to be **beta level** software. API details are subject to change however at this point it is unlikely for there to be significant backwards-incompatible changes. https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html
[^5]: Test results as of [today's date, e.g., August 20, 2023].
