from asyncio import current_task

from sqlalchemy.ext.asyncio import (  # AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from .. import IS_TEST, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ECHO, SQLALCHEMY_ISOLATION_LEVEL
from ..test import pytest_scope_func
from .base import get_parsed_database_uri

AsyncMySQLEngine = create_async_engine(
    get_parsed_database_uri(SQLALCHEMY_DATABASE_URI),
    echo=SQLALCHEMY_ECHO,
    isolation_level=SQLALCHEMY_ISOLATION_LEVEL,
)

AsyncMySQLScopedSession = async_scoped_session(
    sessionmaker(
        AsyncMySQLEngine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    ),
    scopefunc=current_task if not IS_TEST else pytest_scope_func,
)
