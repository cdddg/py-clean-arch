from typing import Optional

import strawberry

from common.type import PokemonNumberStr, UUIDStr


@strawberry.input
class CreatePokemonInput:
    no: str = strawberry.field(description=PokemonNumberStr.__doc__)
    name: str
    type_names: list[str]
    before_evolution_numbers: Optional[list[str]] = strawberry.field(
        default=None, description=PokemonNumberStr.__doc__
    )
    after_evolution_numbers: Optional[list[str]] = strawberry.field(
        default=None, description=PokemonNumberStr.__doc__
    )


@strawberry.input
class UpdatePokemonInput:
    name: Optional[str] = None
    type_names: Optional[list[str]] = None
    before_evolution_numbers: Optional[list[str]] = strawberry.field(
        default=None, description=PokemonNumberStr.__doc__
    )
    after_evolution_numbers: Optional[list[str]] = strawberry.field(
        default=None, description=PokemonNumberStr.__doc__
    )


@strawberry.type
class PokemonNode:
    no: str = strawberry.field(description=PokemonNumberStr.__doc__)
    name: str
    types: list['TypeNode']
    before_evolutions: list['EvolutionNode']
    after_evolutions: list['EvolutionNode']


@strawberry.type
class TypeNode:
    id: str = strawberry.field(description=UUIDStr.__doc__)
    name: str


@strawberry.type
class EvolutionNode:
    no: str = strawberry.field(description=PokemonNumberStr.__doc__)
    name: str
