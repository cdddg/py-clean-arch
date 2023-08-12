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
