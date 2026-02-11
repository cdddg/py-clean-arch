import strawberry

from common.type import PokemonNumberStr, UUIDStr


@strawberry.input
class CreateTrainerInput:
    name: str
    region: str
    badge_count: int = 0


@strawberry.input
class UpdateTrainerInput:
    name: str | None = None
    region: str | None = None
    badge_count: int | None = None


@strawberry.input
class CatchPokemonInput:
    pokemon_no: str = strawberry.field(description=PokemonNumberStr.__doc__)


@strawberry.input
class ReleasePokemonInput:
    pokemon_no: str = strawberry.field(description=PokemonNumberStr.__doc__)


@strawberry.input
class TradePokemonInput:
    trainer_id: str = strawberry.field(description=UUIDStr.__doc__)
    other_trainer_id: str = strawberry.field(description=UUIDStr.__doc__)
    pokemon_no: str = strawberry.field(description=PokemonNumberStr.__doc__)
    other_pokemon_no: str = strawberry.field(description=PokemonNumberStr.__doc__)


@strawberry.type
class TrainerPokemonNode:
    no: str = strawberry.field(description=PokemonNumberStr.__doc__)
    name: str


@strawberry.type
class TrainerNode:
    id: str = strawberry.field(description=UUIDStr.__doc__)
    name: str
    region: str
    badge_count: int
    team: list[TrainerPokemonNode]


@strawberry.type
class TradeNode:
    trainer: TrainerNode
    other_trainer: TrainerNode
