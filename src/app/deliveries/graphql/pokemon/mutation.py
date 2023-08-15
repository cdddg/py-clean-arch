from typing import Annotated

import strawberry
from strawberry.types import Info

import app.usecases.pokemon as pokemon_ucase

from .schema import CreatePokemonInput, PokemonNode, UpdatePokemonInput


@strawberry.type
class Mutation:
    @strawberry.field
    async def create_pokemon(
        self,
        input_: Annotated[CreatePokemonInput, strawberry.argument(name='input')],
        _: Info,
    ) -> PokemonNode:
        pokemon = await pokemon_ucase.create_pokemon(input_.to_instance())

        return PokemonNode.from_instance(pokemon)

    @strawberry.field
    async def update_pokemon(
        self,
        no: str,
        input_: Annotated[UpdatePokemonInput, strawberry.argument(name='input')],
        _: Info,
    ) -> PokemonNode:
        pokemon = await pokemon_ucase.update_pokemon(no, input_.to_instance())

        return PokemonNode.from_instance(pokemon)

    @strawberry.field
    async def delete_pokemon(self, no: str, _: Info) -> None:
        await pokemon_ucase.delete_pokemon(no)
