"""
Dependency Injection Configuration for the Application.

This module sets up dependency injection for database interactions within the
application. It accommodates both relational and NoSQL databases, providing the
flexibility needed for various database integrations based on application
requirements.

The Injector is tailored with specific modules depending on the database type
specified by environment variables. Each module offers essential components such
as sessions, repositories, and units of work necessary for database operations.

Usage:
    # To obtain a unit of work for database operations, use the following:
    async_unit_of_work = injector.get(AbstractUnitOfWork)

For detailed guidance and advanced use cases of dependency injection in Python,
refer to:
- https://github.com/python-injector/injector
- https://github.com/ets-labs/python-dependency-injector
- https://github.com/ivankorobkov/python-inject
"""

# pylint: disable=import-outside-toplevel


from injector import Injector, Module, inject, provider, singleton
from motor.motor_asyncio import AsyncIOMotorCollection
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.nosql import MongoDBPokemonRepository
from repositories.relational_db import RelationalDBPokemonRepository
from settings.db import IS_NOSQL, IS_RELATIONAL_DB

from .unit_of_work import AbstractUnitOfWork, AsyncMotorUnitOfWork, AsyncSqlAlchemyUnitOfWork


class RelationalDBModule(Module):
    @provider
    def provide_async_session(self) -> AsyncSession:
        from settings.db import AsyncScopedSession

        return AsyncScopedSession()

    @provider
    @inject
    def provide_pokemon_repository(self, session: AsyncSession) -> RelationalDBPokemonRepository:
        return RelationalDBPokemonRepository(session)

    @provider
    @inject
    def provide_async_sqlalchemy_unit_of_work(
        self, session: AsyncSession, pokemon_repo: RelationalDBPokemonRepository
    ) -> AbstractUnitOfWork:
        return AsyncSqlAlchemyUnitOfWork(session, pokemon_repo)


class NoSQLModule(Module):
    @singleton
    @provider
    def provide_async_mongo_collection(self) -> AsyncIOMotorCollection:
        from settings.db.mongodb import COLLECTION_NAME, DATABASE_NAME, AsyncMongoDBEngine

        return AsyncMongoDBEngine[DATABASE_NAME][COLLECTION_NAME]

    @provider
    @inject
    def provide_pokemon_repository(
        self, collection: AsyncIOMotorCollection
    ) -> MongoDBPokemonRepository:
        return MongoDBPokemonRepository(collection, session=None)

    @provider
    def provide_async_motor_unit_of_work(
        self, pokemon_repo: MongoDBPokemonRepository
    ) -> AbstractUnitOfWork:
        from settings.db.mongodb import AsyncMongoDBEngine

        return AsyncMotorUnitOfWork(AsyncMongoDBEngine, pokemon_repo)


if IS_RELATIONAL_DB:
    injector = Injector([RelationalDBModule()])
elif IS_NOSQL:
    injector = Injector([NoSQLModule()])
else:
    raise RuntimeError('Invalid database type configuration. It\'s neither relational nor NoSQL')
