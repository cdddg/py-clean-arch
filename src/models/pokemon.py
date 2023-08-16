from dataclasses import dataclass, field
from typing import Optional

from common.type import UUIDStr


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
    no: str
    name: str


@dataclass
class GetPokemonParamsModel:
    offset: int = 0
    limit: Optional[int] = None


@dataclass
class CreatePokemonModel:
    no: str
    name: str
    type_names: list[str]
    before_evolution_numbers: list[str]
    after_evolution_numbers: list[str]


@dataclass
class UpdatePokemonModel:
    name: Optional[str] = None
    type_names: Optional[list[str]] = None
    before_evolution_numbers: Optional[list[str]] = None
    after_evolution_numbers: Optional[list[str]] = None


@dataclass
class PokemonModel:
    no: str
    name: str
    types: list[TypeModel] = field(default_factory=list)
    before_evolutions: list[PokemonEvolutionModel] = field(default_factory=list)
    after_evolutions: list[PokemonEvolutionModel] = field(default_factory=list)
