import abc
from abc import abstractmethod
from typing import Any, Generic, Optional, Type, TypeVar

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.abstraction import AbstractPokemonRepository
from repositories.nosql import MongoDBPokemonRepository
from repositories.relational_db import RelationalDBPokemonRepository

# pylint: disable=import-outside-toplevel,attribute-defined-outside-init


T = TypeVar('T', bound=AbstractPokemonRepository)


class AbstractUnitOfWork(Generic[T], abc.ABC):
    pokemon_repo: AbstractPokemonRepository

    def __init__(self, pokemon_repo: T):
        self.pokemon_repo = pokemon_repo

    @abstractmethod
    async def __aenter__(self) -> 'AbstractUnitOfWork[T]':
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplementedError


class AsyncSqlAlchemyUnitOfWork(AbstractUnitOfWork[RelationalDBPokemonRepository]):
    def __init__(self, session: AsyncSession, pokemon_repo: RelationalDBPokemonRepository):
        super().__init__(pokemon_repo)
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Any
    ) -> None:
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()
            await self.remove()

    async def remove(self):
        # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.async_scoped_session.remove

        from settings import IS_TESTING
        from settings.db import AsyncScopedSession

        if not IS_TESTING:
            await AsyncScopedSession.remove()


class AsyncMotorUnitOfWork(AbstractUnitOfWork[MongoDBPokemonRepository]):
    def __init__(self, engine: AsyncIOMotorClient, pokemon_repo: MongoDBPokemonRepository):
        super().__init__(pokemon_repo)
        self._engine = engine

    async def __aenter__(self):
        self._session = await self._engine.start_session()
        self._session.start_transaction()
        self.pokemon_repo.session = self._session

        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Any
    ) -> None:
        try:
            if exc_type is None:
                await self._session.commit_transaction()
            else:
                await self._session.abort_transaction()
        finally:
            await self._session.end_session()
