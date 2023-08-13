"""
Dependency Injection Configuration for the Application.

For specialized or more advanced requirements, consider some of the recommended DI tools within the Python community:
    - https://github.com/python-injector/injector
    - https://github.com/ets-labs/python-dependency-injector
    - https://github.com/ivankorobkov/python-inject

Usage:
     from dependency_injection import async_unit_of_work
"""


from pkg.repositories.rdbms.pokemon.repository import (
    EvolutionRepository,
    PokemonRepository,
    TypeRepository,
)
from settings.unit_of_work import AsyncSqlAlchemyUnitOfWork


def create_async_sqlalchemy_uow() -> AsyncSqlAlchemyUnitOfWork:
    return AsyncSqlAlchemyUnitOfWork(
        PokemonRepository,
        TypeRepository,
        EvolutionRepository,
    )


async_unit_of_work = create_async_sqlalchemy_uow
