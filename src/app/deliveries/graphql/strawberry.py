"""
This module provides the base schema configuration for the GraphQL API using the strawberry framework.
"""

from typing import Optional, Union

import strawberry
from strawberry.exceptions import GraphQLError
from strawberry.types import ExecutionContext
from strawberry.utils.logging import StrawberryLogger

from settings import IS_TEST


class Schema(strawberry.Schema):
    def process_errors(
        self,
        errors: list[GraphQLError],
        execution_context: Optional[ExecutionContext] = None,
    ):
        # https://github.com/strawberry-graphql/strawberry/issues/847
        # https://github.com/strawberry-graphql/strawberry/pull/851

        for error in errors:
            _error: Union[Exception, GraphQLError] = error
            if isinstance(error, GraphQLError) and error.original_error:
                _error = error.original_error
            if IS_TEST:
                raise _error

            error.message = f'{type(_error).__name__}: {error.message}'
            StrawberryLogger.error(error, execution_context)
