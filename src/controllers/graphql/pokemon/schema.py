import strawberry

from common.type import PokemonNumberStr, UUIDStr


@strawberry.input
class CreatePokemonInput:
    no: str = strawberry.field(description=PokemonNumberStr.__doc__)
    name: str
    type_names: list[str]
    previous_evolution_numbers: list[str] | None = strawberry.field(
        default_factory=list, description=PokemonNumberStr.__doc__
    )
    next_evolution_numbers: list[str] | None = strawberry.field(
        default_factory=list, description=PokemonNumberStr.__doc__
    )


@strawberry.input
class UpdatePokemonInput:
    name: str | None = None
    type_names: list[str] | None = None
    previous_evolution_numbers: list[str] | None = strawberry.field(
        default=None, description=PokemonNumberStr.__doc__
    )
    next_evolution_numbers: list[str] | None = strawberry.field(
        default=None, description=PokemonNumberStr.__doc__
    )


@strawberry.type
class PokemonNode:
    no: str = strawberry.field(description=PokemonNumberStr.__doc__)
    name: str
    types: list['TypeNode']
    previous_evolutions: list['EvolutionNode']
    next_evolutions: list['EvolutionNode']


@strawberry.type
class TypeNode:
    id: str = strawberry.field(description=UUIDStr.__doc__)
    name: str


@strawberry.type
class EvolutionNode:
    no: str = strawberry.field(description=PokemonNumberStr.__doc__)
    name: str
