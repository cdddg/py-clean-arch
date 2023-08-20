"""
This module provides utility functions to integrate FastAPI exception handlers with the application's
domain-specific exceptions. It ensures that custom errors in the domain layer are transformed into appropriate
HTTP responses when they propagate to the HTTP layer.
"""

from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from models.exception import PokedexError, PokemonNotFound, PokemonUnknownError


def handle_custom_error(
    request: Request,
    exc: Union[PokedexError, PokemonNotFound, PokemonUnknownError],
) -> JSONResponse:
    return JSONResponse({'error': f'{type(exc).__name__}: {exc}'}, status_code=400)


def add_exception_handlers(app: FastAPI):
    for exc in (PokedexError, PokemonNotFound, PokemonUnknownError):
        app.add_exception_handler(exc, handle_custom_error)
