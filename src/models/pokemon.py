from dataclasses import dataclass, field
from typing import Optional

from common.type import PokemonNumberStr, UUIDStr


@dataclass
class GetTypeParamsModel:
    offset: int = 0
    limit: Optional[int] = None
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
    offset: int = 0
    limit: Optional[int] = None


@dataclass
class CreatePokemonModel:
    no: PokemonNumberStr
    name: str
    type_names: list[str]
    before_evolution_numbers: list[PokemonNumberStr]
    after_evolution_numbers: list[PokemonNumberStr]

    def __post_init__(self):
        self._validate_no_not_in_evolutions()

    def _validate_no_not_in_evolutions(self):
        if self.no in (self.before_evolution_numbers + self.after_evolution_numbers):
            raise ValueError('Pokemon number cannot be the same as any of its evolution numbers')


@dataclass
class UpdatePokemonModel:
    name: Optional[str] = None
    type_names: Optional[list[str]] = None
    before_evolution_numbers: Optional[list[PokemonNumberStr]] = None
    after_evolution_numbers: Optional[list[PokemonNumberStr]] = None

    def validate_no_not_in_evolutions(self, no: PokemonNumberStr):
        if no in ((self.before_evolution_numbers or []) + (self.after_evolution_numbers or [])):
            raise ValueError('Pokemon number cannot be the same as any of its evolution numbers')


@dataclass
class PokemonModel:
    no: PokemonNumberStr
    name: str
    types: list[TypeModel] = field(default_factory=list)
    before_evolutions: list[PokemonEvolutionModel] = field(default_factory=list)
    after_evolutions: list[PokemonEvolutionModel] = field(default_factory=list)
