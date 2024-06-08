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


from injector import Injector, Module, provider, singleton
from motor.motor_asyncio import AsyncIOMotorCollection
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.document_db import MongoDBPokemonRepository
from repositories.key_value_db import RedisPokemonRepository
from repositories.relational_db import RelationalDBPokemonRepository
from settings.db import IS_DOCUMENT_DB, IS_KEY_VALUE_DB, IS_RELATIONAL_DB

from .unit_of_work import (
    AbstractUnitOfWork,
    AsyncMotorUnitOfWork,
    AsyncRedisUnitOfWork,
    AsyncSQLAlchemyUnitOfWork,
)


class RelationalDBModule(Module):
    @provider
    def provide_async_session(self) -> AsyncSession:
        """Provides an instance of AsyncSession for database operations within an asynchronous context.

        This function is designed to return a scoped session that is unique to the current asyncio task,
        utilizing `asyncio.current_task` as its scope function. This ensures that within a single asyncio task,
        repeated calls to this provider will yield the same AsyncSession instance, promoting session reuse
        and consistency across database operations initiated within the same task context.

        However, it's observed that `provide_async_session` can be invoked multiple times, leading to
        the creation of multiple session instances. This behavior is mitigated by the underlying mechanism
        that binds session instances to the current asyncio task, thus ensuring that within the asyncio
        context, these invocations will still resolve to the same AsyncSession instance.

        Should concerns arise regarding this behavior or if an alternative dependency injection pattern
        is preferred, consider adjusting the session management strategy or exploring other DI tools
        that might offer more granular control over session lifecycle and task scoping.

        Note: The effectiveness of this pattern relies on the proper functioning of `asyncio.current_task`
        for identifying and segregating sessions per task. Misuse or misconfiguration could lead to
        unintended session sharing or leakage across tasks. Ensure thorough testing and understanding
        of the async context and task management in your application.

        Invocation example for obtaining an AbstractUnitOfWork, illustrating the call sequence:

        ```
        injector.get(AbstractUnitOfWork)
            |-> provide_async_session()
            |-> provide_async_session()  # This call reuses the session from the first invocation within the same asyncio task.
            |-> provide_pokemon_repository()
            |-> provide_async_sqlalchemy_unit_of_work()
        ```
        """
        from settings.db import get_async_session

        return get_async_session()

    @provider
    def provide_pokemon_repository(self, session: AsyncSession) -> RelationalDBPokemonRepository:
        return RelationalDBPokemonRepository(session)

    @provider
    def provide_async_sqlalchemy_unit_of_work(
        self, session: AsyncSession, pokemon_repo: RelationalDBPokemonRepository
    ) -> AbstractUnitOfWork:
        return AsyncSQLAlchemyUnitOfWork(session, pokemon_repo)


class DocumentDBModule(Module):
    @singleton
    @provider
    def provide_async_mongo_collection(
        self,
    ) -> AsyncIOMotorCollection:  # pyright: ignore[reportInvalidTypeForm]
        from settings.db.mongodb import COLLECTION_NAME, DATABASE_NAME, AsyncMongoDBEngine

        return AsyncMongoDBEngine[DATABASE_NAME][COLLECTION_NAME]

    @provider
    def provide_pokemon_repository(
        self,
        collection: AsyncIOMotorCollection,  # pyright: ignore[reportInvalidTypeForm]
    ) -> MongoDBPokemonRepository:
        return MongoDBPokemonRepository(collection, session=None)

    @provider
    def provide_async_motor_unit_of_work(
        self, pokemon_repo: MongoDBPokemonRepository
    ) -> AbstractUnitOfWork:
        from settings.db.mongodb import AsyncMongoDBEngine

        return AsyncMotorUnitOfWork(AsyncMongoDBEngine, pokemon_repo)


class KeyValueDBModule(Module):
    @provider
    def provide_async_motor_unit_of_work(self) -> AbstractUnitOfWork:
        from settings.db import get_async_client

        client = get_async_client()
        pokemon_repo = RedisPokemonRepository(client)

        return AsyncRedisUnitOfWork(client, pokemon_repo)


class DatabaseModuleFactory:
    def create_module(self):
        if IS_RELATIONAL_DB:
            return RelationalDBModule()
        if IS_DOCUMENT_DB:
            return DocumentDBModule()
        if IS_KEY_VALUE_DB:
            return KeyValueDBModule()

        raise RuntimeError(
            'Invalid database type configuration. It\'s neither relational nor NoSQL'
        )


injector = Injector([DatabaseModuleFactory().create_module()])
