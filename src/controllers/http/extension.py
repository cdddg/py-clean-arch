"""
Extensions for Controller Layer.

This module provides utility functions to integrate FastAPI exception handlers with the application's
domain-specific exceptions. It ensures that custom errors in the domain layer are transformed into appropriate
HTTP responses when they propagate to the HTTP layer.

Note:
    For simpler requirements, use extension.py. For more complex needs, consider extensions/$package.py for better clarity and scalability.
"""


from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models.exception import (
    PokemonAlreadyExists,
    PokemonError,
    PokemonNotFound,
    PokemonUnknownError,
)


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(PokemonError)
    @app.exception_handler(PokemonUnknownError)
    async def handle_general_pokemon_error(_, exc):
        return JSONResponse(content={'error': f'{type(exc).__name__}: {exc}'}, status_code=400)

    @app.exception_handler(PokemonNotFound)
    async def handle_pokemon_not_found_error(_, exc):
        return JSONResponse(content={'error': f'{type(exc).__name__}: {exc}'}, status_code=404)

    @app.exception_handler(PokemonAlreadyExists)
    async def handle_pokemon_already_exists_error(_, exc):
        return JSONResponse(content={'error': f'{type(exc).__name__}: {exc}'}, status_code=409)
