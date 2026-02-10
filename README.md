# py-clean-arch

This Python project showcases the implementation of a Pokémon API following the Clean Architecture principles, built with the FastAPI framework. It serves as a practical example of how Clean Architecture enables swapping infrastructure — databases, API protocols — without changing business logic.

## Description

The Clean Architecture, popularized by **[Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)**, emphasizes several foundational principles:

1. **Framework Independence**: The system isn't reliant on external libraries or frameworks.
2. **Testability**: Business rules can be validated without any external elements.
3. **UI Independence**: Switching out the user interface won't affect the underlying system.
4. **Database Independence**: The system's business logic isn't tied to a specific database.
5. **Independence from External Agencies**: The business logic remains agnostic of external integrations.

![clean-arch-01](./docs/clean-arch-01.png)
\*source: [yoan-thirion.gitbook.io](https://yoan-thirion.gitbook.io/knowledge-base/software-craftsmanship/code-katas/clean-architecture)

### 🧱 Project Structure Overview & Clean Architecture Mapping

Based on Uncle Bob's Clean Architecture principles, this project's structure and architecture flow diagrams are aligned with these principles.

#### Directory Structure

Here's a glimpse of the project's high-level structure, highlighting primary directories and key files:

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
│   ├── repositories/         - Data interaction layer, converting domain data to/from database format.
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

#### Clean Architecture Flow Diagram

The Clean Architecture Flow Diagram visualizes the layers of Clean Architecture and how they interact. It consists of two images and an ASCII flow for clarity:

> For a detailed explanation of the ASCII flow, refer to **[ascii-flow.md](./docs/ascii-flow.md)**.

![clean-arch-02](./docs/clean-arch-02.png)
\*source: [yoan-thirion.gitbook.io](https://yoan-thirion.gitbook.io/knowledge-base/software-craftsmanship/code-katas/clean-architecture)

![clean-arch-03](./docs/clean-arch-03.png)
\*source: https://stackoverflow.com/a/73788685

### 🔀 Design Decisions

Both **REST and GraphQL** share the same usecases layer, showing that the API protocol can change independently. Similarly, **5 databases** (SQLite, MySQL, PostgreSQL, MongoDB, Redis) run behind the same `AbstractPokemonRepository`, proving that storage can be swapped without touching business logic. In practice, you would pick one protocol and one database.

This is enabled by several design patterns:

- **Repository Pattern** [^1] — decouples the model layer from data storage
- **Unit of Work Pattern** [^2] — ensures transactional consistency
- **Dependency Injection** [^3] — reduces coupling between modules
- **Asynchronous SQLAlchemy 2.0** [^4] — async database operations

To keep the focus on architecture, this project makes several deliberate simplifications:

- Database credentials are hardcoded in `docker-compose.yml` — production requires secrets management
- Error responses expose full exception details — production should use standardized error codes
- GraphQL loads all relations regardless of requested fields ([optimization notes](./src/controllers/graphql/pokemon/query.py)) — production would use the DataLoader pattern
- Database engines initialize at import time — larger apps benefit from lazy initialization

For deeper discussion, see the **[FAQ](./docs/faq.md)**.

## Getting Started

Get this project up and running on your local machine for development and testing.

### ⚡︎ Quick Start

Start the application with a single command — no local Python or dependency installation required:

```sh
$ docker compose up app
```

The app starts with an **in-memory SQLite** database by default. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) and try the interactive endpoints.

![fastapi-doc](./docs/fastapi-swagger.png)

### 🐳 Database Options

Choose from multiple supported database types:

<a id="supported-database-uris"></a>

**Supported Database URIs:**

- `sqlite+aiosqlite:///<dbname>.db` (SQLite)
- `sqlite+aiosqlite:///:memory:` (In-Memory SQLite) - **Default**
- `mysql+asyncmy://<username>:<password>@<host>:<port>/<dbname>` (MySQL)
- `postgresql+asyncpg://<username>:<password>@<host>:<port>/<dbname>` (PostgreSQL)
- `mongodb://<username>:<password>@<host>:<port>/<dbname>` (MongoDB)
- `redis://<username>:<password>@<host>:<port>/<dbname>` (Redis)

> 📌 **Note**: If you encounter database initialization issues, append **`reinitialize=true`** to the `DATABASE_URI`, e.g., `sqlite+aiosqlite:///sqlite.db?reinitialize=true`.

**Start databases with Docker Compose:**
```sh
$ docker compose down --remove-orphans -v
$ docker compose up dockerize
```

### 🔧 Development Setup

For local development with hot-reload, set up the environment directly on your machine:

1. **Install prerequisites:** <u>Python 3.11+</u> and <u>[uv](https://docs.astral.sh/uv/)</u>

2. **Configure your environment:** [^6]

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

#### Single Database Testing

Test against a specific database by setting the `DATABASE_URI` environment variable:

```sh
$ DATABASE_URI=<database-uri> uv run pytest
```

> For supported database URIs, see [**Database Options**](#supported-database-uris)
>
> 📌 **Note**: Use a different `dbname` with "\_test" suffix for testing (e.g., "mydatabase_test") to avoid interfering with your main application data.

#### Multi-Database Testing with Coverage [^5]

Run `pytest` against each supported database (SQLite, MySQL, PostgreSQL, MongoDB, Redis) in separate processes using `bats`:

1. **Install bats:** Follow the [installation guide](https://bats-core.readthedocs.io/en/stable/installation.html)

2. **Run comprehensive tests:**

   ```shell
   $ make test
   ```


## Changelog

See the full version history in **[CHANGELOG.md](./CHANGELOG.md).**

## Enjoying the Project .ᐣ

If this project helped you, a ⭐ would be greatly appreciated!<br>
Have questions or ideas? Feel free to [open an issue](https://github.com/cdddg/py-clean-arch/issues) or submit a PR.

[^1]: https://www.cosmicpython.com/book/chapter_02_repository.html

[^2]: https://www.cosmicpython.com/book/chapter_06_uow.html

[^3]: https://en.wikipedia.org/wiki/Dependency_injection

[^4]: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

[^5]: The coverage rate for this 'py-clean-arch' project stands at 95.55%, based on test results from February 9, 2026.

[^6]: The `uv sync` command installs all required packages for running and developing the application. However, it does not include `cspell`. If you need `cspell` for spell checking, please refer to the official installation guide at [cspell installation guide](https://cspell.org/docs/installation/)
