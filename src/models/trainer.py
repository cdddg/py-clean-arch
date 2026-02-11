from dataclasses import dataclass, field

from common.type import PokemonNumberStr, UUIDStr

MAX_TEAM_SIZE = 6


@dataclass
class TrainerPokemonModel:
    no: PokemonNumberStr
    name: str


@dataclass
class TrainerModel:
    id: UUIDStr
    name: str
    region: str
    badge_count: int
    team: list[TrainerPokemonModel] = field(default_factory=list)

    @property
    def is_team_full(self) -> bool:
        return len(self.team) >= MAX_TEAM_SIZE

    def has_pokemon(self, pokemon_no: PokemonNumberStr) -> bool:
        return any(p.no == pokemon_no for p in self.team)


@dataclass
class CreateTrainerModel:
    name: str
    region: str
    badge_count: int


@dataclass
class UpdateTrainerModel:
    name: str | None = None
    region: str | None = None
    badge_count: int | None = None


@dataclass
class CatchPokemonModel:
    pokemon_no: PokemonNumberStr


@dataclass
class ReleasePokemonModel:
    pokemon_no: PokemonNumberStr


@dataclass
class TradePokemonModel:
    trainer_id: UUIDStr
    other_trainer_id: UUIDStr
    pokemon_no: PokemonNumberStr
    other_pokemon_no: PokemonNumberStr
