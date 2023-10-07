"""
Dependency Injection Configuration for the Application.

This module handles the setup and configuration for database interactions in the application.
The current architecture is designed with the flexibility to support multiple databases in the future.
All related database packages are imported for this purpose.
However, as a best practice, if a specific database becomes unnecessary, 
its associated code should be removed to streamline and maintain the clarity of the application.

For specialized or more advanced requirements, consider some of the recommended DI tools within the Python community:
    - https://github.com/python-injector/injector
    - https://github.com/ets-labs/python-dependency-injector
    - https://github.com/ivankorobkov/python-inject

Usage:
     from dependency_injection import async_unit_of_work
"""


from app.repositories.nosql.pokemon.repository import MongoDBPokemonRepository
from app.repositories.relational_db.pokemon.repository import RelationalDBPokemonRepository
from settings.db import IS_NOSQL, IS_RELATIONAL_DB

from .unit_of_work import AsyncMotorUnitOfWork, AsyncSqlAlchemyUnitOfWork


def create_async_sqlalchemy_uow() -> AsyncSqlAlchemyUnitOfWork:
    return AsyncSqlAlchemyUnitOfWork(RelationalDBPokemonRepository)


def create_async_motor_uow() -> AsyncMotorUnitOfWork:
    return AsyncMotorUnitOfWork(MongoDBPokemonRepository)


if IS_RELATIONAL_DB:
    async_unit_of_work = create_async_sqlalchemy_uow
elif IS_NOSQL:
    async_unit_of_work = create_async_motor_uow
else:
    raise RuntimeError('Invalid database type configuration. It\'s neither relational nor NoSQL')
