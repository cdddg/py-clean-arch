import strawberry
from strawberry.types import Info

import pkg.usecases.pokemon as pokemon_ucase

from .schema import PokemonNode


@strawberry.type
class Query:
    @strawberry.field
    async def pokemons(self, _: Info) -> list[PokemonNode]:
        pokemons = await pokemon_ucase.get_pokemons()

        return list(map(PokemonNode.from_instance, pokemons))

    @strawberry.field
    async def pokemon(self, no: str, _: Info) -> PokemonNode:
        pokemon = await pokemon_ucase.get_pokemon(no)

        return PokemonNode.from_instance(pokemon)
