from typing import Annotated

import strawberry
from strawberry.types import Info

import usecases.pokemon as pokemon_ucase
from common.type import PokemonNumberStr
from di.dependency_injection import injector
from di.unit_of_work import AbstractUnitOfWork

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
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        create_pokemon_data = PokemonInputMapper.create_input_to_entity(input_)
        created_pokemon = await pokemon_ucase.create_pokemon(
            async_unit_of_work, create_pokemon_data
        )

        return PokemonNodeMapper.entity_to_node(created_pokemon)

    @strawberry.field
    async def update_pokemon(
        self,
        no: Annotated[str, strawberry.argument(description=PokemonNumberStr.__doc__)],
        input_: Annotated[UpdatePokemonInput, strawberry.argument(name='input')],
        _: Info,
    ) -> PokemonNode:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        no = PokemonNumberStr(no)
        update_pokemon_data = PokemonInputMapper.update_input_to_entity(input_)
        updated_pokemon = await pokemon_ucase.update_pokemon(
            async_unit_of_work, no, update_pokemon_data
        )

        return PokemonNodeMapper.entity_to_node(updated_pokemon)

    @strawberry.field
    async def delete_pokemon(
        self,
        no: Annotated[str, strawberry.argument(description=PokemonNumberStr.__doc__)],
        _: Info,
    ) -> None:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        no = PokemonNumberStr(no)
        await pokemon_ucase.delete_pokemon(async_unit_of_work, no)
