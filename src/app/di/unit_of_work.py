from typing import Any, Optional, Type

from app.repositories.nosql.pokemon.repository import MongoDBPokemonRepository
from app.repositories.relational_db.pokemon.repository import RelationalDBPokemonRepository


# pylint: disable=attribute-defined-outside-init,import-outside-toplevel
class AsyncSqlAlchemyUnitOfWork:
    def __init__(self, pokemon_repo_cls: Type[RelationalDBPokemonRepository]):
        from settings.db import AsyncScopedSession

        self._pokemon_repo_cls = pokemon_repo_cls
        self._session = AsyncScopedSession()

    @property
    def pokemon_repo(self):
        if not hasattr(self, '_pokemon_repo'):
            self._pokemon_repo = self._pokemon_repo_cls(self._session)
        return self._pokemon_repo

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


class AsyncMotorUnitOfWork:
    def __init__(self, pokemon_repo_cls: Type[MongoDBPokemonRepository]):
        from settings.db import COLLECTION_NAME, DATABASE_NAME, AsyncMongoDBEngine

        self._pokemon_repo_cls = pokemon_repo_cls
        self._collection = AsyncMongoDBEngine[DATABASE_NAME][COLLECTION_NAME]

    @property
    def pokemon_repo(self):
        if not hasattr(self, '_pokemon_repo'):
            self._pokemon_repo = self._pokemon_repo_cls(self._collection, self._session)
        else:
            self._pokemon_repo.session = self._session

        return self._pokemon_repo

    async def __aenter__(self):
        from settings.db.mongodb import AsyncMongoDBEngine

        self._session = await AsyncMongoDBEngine.start_session()
        self._session.start_transaction()

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
