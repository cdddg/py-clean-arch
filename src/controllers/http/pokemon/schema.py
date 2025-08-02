from typing import Optional

from pydantic import BaseModel, Field

from common.type import PokemonNumberStr, UUIDStr


class CreatePokemonRequest(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str
    type_names: Optional[list[str]] = None
    previous_evolution_numbers: Optional[list[str]] = Field(
        default=[], description=PokemonNumberStr.__doc__
    )
    next_evolution_numbers: Optional[list[str]] = Field(
        default=[], description=PokemonNumberStr.__doc__
    )


class UpdatePokemonRequest(BaseModel):
    name: Optional[str] = None
    type_names: Optional[list[str]] = None
    previous_evolution_numbers: Optional[list[str]] = Field(
        default=None, description=PokemonNumberStr.__doc__
    )
    next_evolution_numbers: Optional[list[str]] = Field(
        default=None, description=PokemonNumberStr.__doc__
    )


class PokemonResponse(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str
    types: list['TypeResponse']
    previous_evolutions: list['EvolutionResponse']
    next_evolutions: list['EvolutionResponse']


class TypeResponse(BaseModel):
    id: str = Field(..., description=UUIDStr.__doc__)
    name: str


class EvolutionResponse(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str


PokemonResponse.model_rebuild()
