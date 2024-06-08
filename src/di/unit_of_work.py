import abc
from abc import abstractmethod
from typing import Any, Generic, Optional, Type, TypeVar

from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.abstraction import AbstractPokemonRepository
from repositories.document_db import MongoDBPokemonRepository
from repositories.key_value_db import RedisPokemonRepository
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


class AsyncSQLAlchemyUnitOfWork(AbstractUnitOfWork[RelationalDBPokemonRepository]):
    def __init__(self, session: AsyncSession, pokemon_repo: RelationalDBPokemonRepository):
        super().__init__(pokemon_repo)
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Any
    ):
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()
            await self.remove()

    async def remove(self):
        from settings.db import AsyncScopedSession

        # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.async_scoped_session.remove
        await AsyncScopedSession.remove()


class AsyncMotorUnitOfWork(AbstractUnitOfWork[MongoDBPokemonRepository]):
    def __init__(
        self,
        engine: AsyncIOMotorClient,  # pyright: ignore[reportInvalidTypeForm]
        pokemon_repo: MongoDBPokemonRepository,
    ):
        super().__init__(pokemon_repo)
        self._engine = engine

    async def __aenter__(self):
        self._session = await self._engine.start_session()
        self._session.start_transaction()
        self.pokemon_repo.session = self._session

        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Any
    ):
        try:
            if exc_type is None:
                await self._session.commit_transaction()
            else:
                await self._session.abort_transaction()
        finally:
            await self._session.end_session()


class AsyncRedisUnitOfWork(AbstractUnitOfWork[RedisPokemonRepository]):
    """
    This implementation does not support transactions.

    If transaction-like behavior is required, compensating actions must be implemented manually.

    Compensating actions are a series of operations that revert the effects of the preceding operations
    in case of failure, ensuring data consistency.

    For more information, see: https://en.wikipedia.org/wiki/Compensating_transaction
    """

    def __init__(self, client: AsyncRedis, pokemon_repo: RedisPokemonRepository):
        self._client = client
        super().__init__(pokemon_repo)

    async def __aenter__(self):
        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Any
    ) -> None:
        # Not supported yet, see https://github.com/python/typeshed/blob/main/stubs/redis/redis/asyncio/client.pyi#L27
        await self._client.aclose()  # type: ignore
