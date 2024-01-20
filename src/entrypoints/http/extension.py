"""
Extensions for Entrypoint Layer.

This module provides utility functions to integrate FastAPI exception handlers with the application's
domain-specific exceptions. It ensures that custom errors in the domain layer are transformed into appropriate
HTTP responses when they propagate to the HTTP layer.

Note:
    For simpler requirements, use extension.py. For more complex needs, consider extensions/$package.py for better clarity and scalability.
"""

from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from models.exception import (
    PokemonAlreadyExists,
    PokemonError,
    PokemonNotFound,
    PokemonUnknownError,
)


def handle_custom_error(
    request: Request,
    exc: Union[PokemonError, PokemonNotFound, PokemonUnknownError, PokemonAlreadyExists],
) -> JSONResponse:
    return JSONResponse({'error': f'{type(exc).__name__}: {exc}'}, status_code=400)


def add_exception_handlers(app: FastAPI):
    for exc in (PokemonError, PokemonNotFound, PokemonUnknownError, PokemonAlreadyExists):
        app.add_exception_handler(exc, handle_custom_error)
