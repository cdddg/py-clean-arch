# py-clean-arch

A Python architecture sample that demonstrates [Uncle Bob's Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) through a Pokémon and Trainer API built with FastAPI. The focus is on showing how layers are separated, how dependencies flow inward, and how infrastructure can be swapped at the structural level.

> This is a learning-oriented project, not a production template. For background and common questions, see the [FAQ](./docs/faq.md).

## Architecture

This project applies Clean Architecture with the following practices:

1. **Framework Independence**: FastAPI is confined to the controllers layer — use cases and models have no framework dependency.
2. **Testability**: Business rules in use cases can be tested without HTTP or database.
3. **UI Independence**: REST and GraphQL are interchangeable outer-layer interfaces.
4. **Database Independence**: Multiple databases implement the same repository contracts.
5. **External Independence**: Domain logic does not depend on specific APIs, ORMs, or drivers.

![clean-arch-01](./docs/clean-arch-01.png)
\*source: [yoan-thirion.gitbook.io](https://yoan-thirion.gitbook.io/knowledge-base/software-craftsmanship/code-katas/clean-architecture)

### 🧱 Project Structure

```ini
./
├── ...
├── src/
│   ├── di/                   - Dependency injection configurations for managing dependencies.
│   │   ├── dependency_injection.py
│   │   └── unit_of_work.py
│   │
│   ├── controllers/          - External interfaces like REST & GraphQL endpoints.
│   │   ├── graphql/          - GraphQL components for a flexible API.
│   │   └── rest/             - RESTful API routes and controllers.
│   │                           ('Frameworks and Drivers' and part of 'Interface Adapters' in Clean Architecture)
│   │
│   ├── usecases/             - Contains application-specific business rules and implementations.
│   │                           ('Use Cases' in Clean Architecture)
│   │
│   ├── repositories/         - Data access abstraction layer, responsible for persistence and retrieval of domain data.
│   │   ├── relational_db/    - Operations for relational databases (e.g., SQLite, MySQL, PostgreSQL).
│   │   ├── document_db/      - Operations for document-oriented databases (e.g., MongoDB, CouchDB).
│   │   └── key_value_db/     - Operations for key-value databases (e.g., Redis, Memcached).
│   │                           ('Interface Adapters' in Clean Architecture)
│   │
│   ├── models/               - Domain entities representing the business data.
│   │                           ('Entities' in Clean Architecture)
│   │
│   ├── common/               - Shared code and utilities.
│   ├── settings/
│   │   └── db/               - Database configurations.
│   │                           ('Frameworks and Drivers' in Clean Architecture)
│   │
│   └── main.py               - Main file to launch the application.
│
└── tests/
    ├── api_db_test.bats      - Runs the full pytest suite against each supported database.
    ├── functional/           - Functional tests for testing the overall functionality and behavior of the application.
    ├── integration/          - Integration tests for testing module interactions.
    └── unit/                 - Unit tests for testing individual components in isolation.
```

### 🧬 What This Sample Demonstrates

**REST and GraphQL** share the same use cases layer — the API protocol is an outer-layer detail. **5 databases** (SQLite, MySQL, PostgreSQL, MongoDB, Redis) sit behind the same repository contracts — storage is also an outer-layer detail.

Two entities illustrate different complexity levels:

- **Pokemon** — basic CRUD
- **Trainer** — business rules like team size limits, ownership checks, and atomic trades

Enabled by several key design decisions:

- **Repository Pattern** [^1] — decouples the model layer from data storage
- **Unit of Work Pattern** [^2] — ensures transactional consistency
- **Dependency Injection** [^3] — reduces coupling between modules
- **Asynchronous SQLAlchemy 2.0** [^4] — async database operations

### 🔄 Flow Diagrams

The flow diagrams visualize the layers and how they interact:

> For a detailed explanation of the ASCII flow, refer to **[ascii-flow.md](./docs/ascii-flow.md)**.

![clean-arch-02](./docs/clean-arch-02.png)
\*source: [yoan-thirion.gitbook.io](https://yoan-thirion.gitbook.io/knowledge-base/software-craftsmanship/code-katas/clean-architecture)

![clean-arch-03](./docs/clean-arch-03.png)
\*source: https://stackoverflow.com/a/73788685

## Getting Started

### ⚡︎ Quick Start

Start the application with a single command — no local Python or dependency installation required:

```sh
$ docker compose up app
```

Uses **in-memory SQLite** by default. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) and try the interactive endpoints.

### 🐳 Database Options

<a id="supported-database-uris"></a>

Set `DATABASE_URI` to switch databases:

| Database        | URI format                                                  |
| --------------- | ----------------------------------------------------------- |
| SQLite (file)   | `sqlite+aiosqlite:///<dbname>.db`                           |
| SQLite (memory) | `sqlite+aiosqlite:///:memory:` **(default)**                |
| MySQL           | `mysql+asyncmy://<user>:<pass>@<host>:<port>/<dbname>`      |
| PostgreSQL      | `postgresql+asyncpg://<user>:<pass>@<host>:<port>/<dbname>` |
| MongoDB         | `mongodb://<user>:<pass>@<host>:<port>/<dbname>`            |
| Redis           | `redis://<user>:<pass>@<host>:<port>/<dbname>`              |

> 📌 **Note**: If you encounter database initialization issues, append **`reinitialize=true`** to the `DATABASE_URI`, e.g., `sqlite+aiosqlite:///sqlite.db?reinitialize=true`.


```sh
$ docker compose down --remove-orphans -v
$ docker compose up dockerize
```

### 🔧 Development Setup

For local development with hot-reload:

1. **Install prerequisites:** <u>Python 3.11+</u> and <u>[uv](https://docs.astral.sh/uv/)</u>

2. **Install dependencies:** [^5]

   ```sh
   $ uv sync
   ```

3. **Launch the application:**

   ```sh
   # With default SQLite database
   $ make up

   # With specific database
   $ DATABASE_URI=<database-uri> make up
   ```

4. **Access the application:** [http://localhost:8000](http://localhost:8000/)

### 🧪 Testing

```sh
# Test against a specific database
$ DATABASE_URI=<database-uri> uv run pytest

# Test against all databases (requires bats)
$ make test
```

> For supported database URIs, see [**Database Options**](#supported-database-uris)
>
> 📌 **Note**: Use a different `dbname` with "\_test" suffix for testing (e.g., "mydatabase_test") to avoid interfering with your main application data.

## Changelog

See the full version history in **[CHANGELOG.md](./CHANGELOG.md).**

## Enjoying the Project .ᐣ

If this project helped you, a ⭐ would be greatly appreciated!<br>
Have questions or ideas? Feel free to [open an issue](https://github.com/cdddg/py-clean-arch/issues) or submit a PR.

[^1]: https://www.cosmicpython.com/book/chapter_02_repository.html

[^2]: https://www.cosmicpython.com/book/chapter_06_uow.html

[^3]: https://en.wikipedia.org/wiki/Dependency_injection

[^4]: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

[^5]: The `uv sync` command installs all required packages for running and developing the application. However, it does not include `cspell`. If you need `cspell` for spell checking, please refer to the official installation guide at [cspell installation guide](https://cspell.org/docs/installation/)
