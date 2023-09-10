from typing import Optional

from pydantic import BaseModel, Field

from common.type import PokemonNumberStr, UUIDStr


class CreatePokemonRequest(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str
    type_names: Optional[list[str]] = None
    before_evolution_numbers: Optional[list[str]] = Field(
        default=[], unique_items=True, description=PokemonNumberStr.__doc__
    )
    after_evolution_numbers: Optional[list[str]] = Field(
        default=[], unique_items=True, description=PokemonNumberStr.__doc__
    )


class UpdatePokemonRequest(BaseModel):
    name: Optional[str]
    type_names: list[str] = []
    before_evolution_numbers: Optional[list[str]] = Field(
        default=[], unique_items=True, description=PokemonNumberStr.__doc__
    )
    after_evolution_numbers: Optional[list[str]] = Field(
        default=[], unique_items=True, description=PokemonNumberStr.__doc__
    )


class PokemonResponse(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str
    types: list['TypeResponse']
    before_evolutions: list['EvolutionResponse']
    after_evolutions: list['EvolutionResponse']


class TypeResponse(BaseModel):
    id: str = Field(..., description=UUIDStr.__doc__)
    name: str


class EvolutionResponse(BaseModel):
    no: str = Field(..., description=PokemonNumberStr.__doc__)
    name: str


PokemonResponse.update_forward_refs()
