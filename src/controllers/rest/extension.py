"""
Extensions for Controller Layer.

This module provides utility functions to integrate FastAPI exception handlers with the application's
domain-specific exceptions. It ensures that custom errors in the domain layer are transformed into appropriate
HTTP responses when they propagate to the REST layer.

Note:
    For simpler requirements, use extension.py. For more complex needs, consider extensions/$package.py for better clarity and scalability.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models.exception import (
    PokemonAlreadyExists,
    PokemonError,
    PokemonNotFound,
    TrainerAlreadyOwnsPokemon,
    TrainerError,
    TrainerNotFound,
)

_EXCEPTION_STATUS_MAP: dict[type[Exception], int] = {
    PokemonNotFound: 404,
    PokemonAlreadyExists: 409,
    TrainerNotFound: 404,
    TrainerAlreadyOwnsPokemon: 409,
}


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(PokemonError)
    @app.exception_handler(TrainerError)
    async def handle_domain_error(_, exc):
        status_code = _EXCEPTION_STATUS_MAP.get(type(exc), 400)
        return JSONResponse(
            content={'error': f'{type(exc).__name__}: {exc}'},
            status_code=status_code,
        )
