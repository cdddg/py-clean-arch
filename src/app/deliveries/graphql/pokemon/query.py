from typing import Annotated

import strawberry
from strawberry.types import Info

import app.usecases.pokemon as pokemon_ucase
from common.type import PokemonNumberStr

from .mapper import PokemonNodeMapper
from .schema import PokemonNode


@strawberry.type
class Query:
    @strawberry.field
    async def pokemons(self, _: Info) -> list[PokemonNode]:
        pokemons = await pokemon_ucase.get_pokemons()

        return list(map(PokemonNodeMapper.entity_to_node, pokemons))

    @strawberry.field
    async def pokemon(
        self,
        no: Annotated[str, strawberry.argument(description=PokemonNumberStr.__doc__)],
        _: Info,
    ) -> PokemonNode:
        pokemon = await pokemon_ucase.get_pokemon(PokemonNumberStr(no))

        return PokemonNodeMapper.entity_to_node(pokemon)
