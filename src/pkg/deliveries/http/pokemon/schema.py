from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, root_validator

from models.pokemon import (
    CreatePokemonModel,
    PokemonEvolutionModel,
    PokemonModel,
    TypeModel,
    UpdatePokemonModel,
)


class CreatePokemonRequest(BaseModel):
    no: str
    name: str
    type_names: list[str] = []
    before_evolution_numbers: list[str] = Field(default=[], unique_items=True)
    after_evolution_numbers: list[str] = Field(default=[], unique_items=True)

    @root_validator()
    def validate_pokemon_numbers(cls, values: dict):
        if values['no'] in (values['before_evolution_numbers'] + values['after_evolution_numbers']):
            raise ValueError('Pokemon number cannot be the same as any of its evolution numbers.')

        return values

    def to_model(self) -> CreatePokemonModel:
        return CreatePokemonModel(
            no=self.no,
            name=self.name,
            type_names=self.type_names,
            before_evolution_numbers=self.before_evolution_numbers,
            after_evolution_numbers=self.after_evolution_numbers,
        )


class UpdatePokemonRequest(BaseModel):
    name: Optional[str]
    type_names: list[str] = []
    before_evolution_numbers: Optional[list[str]] = Field(default=None, unique_items=True)
    after_evolution_numbers: Optional[list[str]] = Field(default=None, unique_items=True)

    def validate_pokemon_number(self, number: str):
        evolution_numbers = (self.before_evolution_numbers or []) + (
            self.after_evolution_numbers or []
        )
        if number in evolution_numbers:
            raise ValueError('Pokemon number cannot be the same as any of its evolution numbers.')

    def to_model(self) -> UpdatePokemonModel:
        kwargs = self.dict(exclude_unset=True)
        return UpdatePokemonModel(**kwargs)


class AddEvolutionRequest(BaseModel):
    evolutions_no: list[str]


class TypeResponse(BaseModel):
    id: UUID
    name: str

    @staticmethod
    def from_model(model: TypeModel) -> 'TypeResponse':
        return TypeResponse(id=model.id, name=model.name)


class EvolutionResponse(BaseModel):
    no: str
    name: str

    @staticmethod
    def from_model(model: PokemonEvolutionModel) -> 'EvolutionResponse':
        return EvolutionResponse(no=model.no, name=model.name)


class PokemonResponse(BaseModel):
    no: str
    name: str
    types: list[TypeResponse]
    before_evolutions: list[EvolutionResponse]
    after_evolutions: list[EvolutionResponse]

    @staticmethod
    def from_model(model: PokemonModel) -> 'PokemonResponse':
        return PokemonResponse(
            no=model.no,
            name=model.name,
            types=list(map(TypeResponse.from_model, model.types)),
            before_evolutions=list(map(EvolutionResponse.from_model, model.before_evolutions)),
            after_evolutions=list(map(EvolutionResponse.from_model, model.after_evolutions)),
        )
