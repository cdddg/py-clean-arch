from dataclasses import dataclass, field
from typing import Optional

from common.type import PokemonNumberStr, UUIDStr


@dataclass
class GetTypeParamsModel:
    page: int = 0
    size: Optional[int] = None
    pokemon_numbers: Optional[list[str]] = None


@dataclass
class TypeModel:
    id: UUIDStr
    name: str


@dataclass
class PokemonEvolutionModel:
    no: PokemonNumberStr
    name: str


@dataclass
class GetPokemonParamsModel:
    page: int = 1
    size: int = 100


@dataclass
class CreatePokemonModel:
    no: PokemonNumberStr
    name: str
    type_names: list[str]
    previous_evolution_numbers: list[PokemonNumberStr]
    next_evolution_numbers: list[PokemonNumberStr]

    def __post_init__(self):
        self._validate_no_not_in_evolutions()

    def _validate_no_not_in_evolutions(self):
        if self.no in (self.previous_evolution_numbers + self.next_evolution_numbers):
            raise ValueError('Pokemon number cannot be the same as any of its evolution numbers')


@dataclass
class UpdatePokemonModel:
    name: Optional[str] = None
    type_names: Optional[list[str]] = None
    previous_evolution_numbers: Optional[list[PokemonNumberStr]] = None
    next_evolution_numbers: Optional[list[PokemonNumberStr]] = None

    def validate_no_not_in_evolutions(self, no: PokemonNumberStr):
        if no in ((self.previous_evolution_numbers or []) + (self.next_evolution_numbers or [])):
            raise ValueError('Pokemon number cannot be the same as any of its evolution numbers')


@dataclass
class PokemonModel:
    no: PokemonNumberStr
    name: str
    types: list[TypeModel] = field(default_factory=list)
    previous_evolutions: list[PokemonEvolutionModel] = field(default_factory=list)
    next_evolutions: list[PokemonEvolutionModel] = field(default_factory=list)
