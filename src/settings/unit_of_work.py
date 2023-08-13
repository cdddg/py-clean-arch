from typing import Type

from pkg.repositories.rdbms.pokemon.repository import (
    EvolutionRepository,
    PokemonRepository,
    TypeRepository,
)
from settings import IS_TEST
from settings.db import AsyncScopedSession


# pylint: disable=attribute-defined-outside-init
class AsyncSqlAlchemyUnitOfWork:
    def __init__(
        self,
        pokemon_repo_cls: Type[PokemonRepository],
        type_repo_cls: Type[TypeRepository],
        evolution_repo_cls: Type[EvolutionRepository],
    ):
        self._pokemon_repo_cls = pokemon_repo_cls
        self._type_repo_cls = type_repo_cls
        self._evolution_repo_cls = evolution_repo_cls
        self._session = AsyncScopedSession()

    @property
    def pokemon_repo(self):
        if not hasattr(self, '_pokemon_repo'):
            self._pokemon_repo = self._pokemon_repo_cls(self._session)
        return self._pokemon_repo

    @property
    def type_repo(self):
        if not hasattr(self, '_type_repo'):
            self._type_repo = self._type_repo_cls(self._session)
        return self._type_repo

    @property
    def evolution_repo(self):
        if not hasattr(self, '_evolution_repo'):
            self._evolution_repo = self._evolution_repo_cls(self._session)
        return self._evolution_repo

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()

        # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.async_scoped_session.remove
        if not IS_TEST:
            await AsyncScopedSession.remove()
