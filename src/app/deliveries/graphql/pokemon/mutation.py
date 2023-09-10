from typing import Annotated

import strawberry
from strawberry.types import Info

import app.usecases.pokemon as pokemon_ucase
from common.type import PokemonNumberStr

from .mapper import PokemonInputMapper, PokemonNodeMapper
from .schema import CreatePokemonInput, PokemonNode, UpdatePokemonInput


@strawberry.type
class Mutation:
    @strawberry.field
    async def create_pokemon(
        self,
        input_: Annotated[CreatePokemonInput, strawberry.argument(name='input')],
        _: Info,
    ) -> PokemonNode:
        pokemon = await pokemon_ucase.create_pokemon(
            PokemonInputMapper.create_input_to_entity(input_)
        )

        return PokemonNodeMapper.entity_to_node(pokemon)

    @strawberry.field
    async def update_pokemon(
        self,
        no: Annotated[str, strawberry.argument(description=PokemonNumberStr.__doc__)],
        input_: Annotated[UpdatePokemonInput, strawberry.argument(name='input')],
        _: Info,
    ) -> PokemonNode:
        pokemon = await pokemon_ucase.update_pokemon(
            PokemonNumberStr(no),
            PokemonInputMapper.update_input_to_entity(input_),
        )

        return PokemonNodeMapper.entity_to_node(pokemon)

    @strawberry.field
    async def delete_pokemon(
        self,
        no: Annotated[str, strawberry.argument(description=PokemonNumberStr.__doc__)],
        _: Info,
    ) -> None:
        await pokemon_ucase.delete_pokemon(PokemonNumberStr(no))
