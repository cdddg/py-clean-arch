from typing import Annotated

import strawberry
from strawberry.types import Info

import usecases.pokemon as pokemon_ucase
from common.type import PokemonNumberStr
from di.dependency_injection import injector
from di.unit_of_work import AbstractUnitOfWork

from .mapper import PokemonNodeMapper
from .schema import PokemonNode


@strawberry.type
class Query:
    @strawberry.field
    async def pokemons(self, _: Info) -> list[PokemonNode]:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        pokemons = await pokemon_ucase.get_pokemons(async_unit_of_work)

        return list(map(PokemonNodeMapper.entity_to_node, pokemons))

    @strawberry.field
    async def pokemon(
        self,
        no: Annotated[str, strawberry.argument(description=PokemonNumberStr.__doc__)],
        _: Info,
    ) -> PokemonNode:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        no = PokemonNumberStr(no)
        pokemon = await pokemon_ucase.get_pokemon(async_unit_of_work, no)

        return PokemonNodeMapper.entity_to_node(pokemon)
