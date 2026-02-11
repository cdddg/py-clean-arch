import abc
from abc import abstractmethod
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.abstraction import AbstractPokemonRepository, AbstractTrainerRepository
from repositories.document_db import MongoDBPokemonRepository, MongoDBTrainerRepository
from repositories.key_value_db import RedisPokemonRepository, RedisTrainerRepository
from repositories.relational_db import RelationalDBPokemonRepository, RelationalDBTrainerRepository

# pylint: disable=import-outside-toplevel,attribute-defined-outside-init


class AbstractUnitOfWork(abc.ABC):
    pokemon_repo: AbstractPokemonRepository
    trainer_repo: AbstractTrainerRepository

    @abstractmethod
    async def __aenter__(self) -> 'AbstractUnitOfWork':
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplementedError


class AsyncSQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        session: AsyncSession,
        pokemon_repo: RelationalDBPokemonRepository,
        trainer_repo: RelationalDBTrainerRepository,
    ):
        self.pokemon_repo = pokemon_repo
        self.trainer_repo = trainer_repo
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any
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


class AsyncMotorUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        engine: AsyncIOMotorClient,  # pyright: ignore[reportInvalidTypeForm]
        pokemon_repo: MongoDBPokemonRepository,
        trainer_repo: MongoDBTrainerRepository,
    ):
        self.pokemon_repo = pokemon_repo
        self.trainer_repo = trainer_repo
        self._engine = engine

    async def __aenter__(self):
        self._session = await self._engine.start_session()
        self._session.start_transaction()
        self.pokemon_repo.session = self._session
        self.trainer_repo.session = self._session

        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any
    ):
        try:
            if exc_type is None:
                await self._session.commit_transaction()
            else:
                await self._session.abort_transaction()
        finally:
            await self._session.end_session()


class AsyncRedisUnitOfWork(AbstractUnitOfWork):
    """
    This implementation does not support transactions.

    If transaction-like behavior is required, compensating actions must be implemented manually.

    Compensating actions are a series of operations that revert the effects of the preceding operations
    in case of failure, ensuring data consistency.

    For more information, see: https://en.wikipedia.org/wiki/Compensating_transaction
    """

    def __init__(
        self,
        client: AsyncRedis,
        pokemon_repo: RedisPokemonRepository,
        trainer_repo: RedisTrainerRepository,
    ):
        self._client = client
        self.pokemon_repo = pokemon_repo
        self.trainer_repo = trainer_repo

    async def __aenter__(self):
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: Any
    ) -> None:
        # Not supported yet, see https://github.com/python/typeshed/blob/main/stubs/redis/redis/asyncio/client.pyi#L27
        await self._client.aclose()  # type: ignore
