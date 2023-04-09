from pkg.repositories.rdbms.pokemon.repository import (
    EvolutionRepository,
    PokemonRepository,
    TypeRepository,
)
from settings import IS_TEST
from settings.db import AsyncScopedSession


class AsyncSqlAlchemyUnitOfWork:
    _pokemon_repo = PokemonRepository
    _type_repo = TypeRepository
    _evolution_repo = EvolutionRepository

    def __init__(self):
        session = AsyncScopedSession()
        self._session = session

        self.pokemon_repo = self._pokemon_repo(session)
        self.type_repo = self._type_repo(session)
        self.evolution_repo = self._evolution_repo(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is None:
            await self._session.commit()
        else:
            await self._session.rollback()
        await self._session.close()

        # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.async_scoped_session.remove
        if not IS_TEST:
            await AsyncScopedSession.remove()
