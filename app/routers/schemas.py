from typing import Dict, List, Optional

from pydantic import BaseModel


class CreatePokemonParames(BaseModel):
    no: str
    name: str
    types: List[str]


class UpdatePokemonParams(BaseModel):
    name: Optional[str]
    types: Optional[List[str]]


class AddEvolutionParams(BaseModel):
    class EvolutionNode(BaseModel):
        pokemon_no: str
        sequence: int

    evolutions: List[EvolutionNode]


class HTTPBadRequest(BaseModel):
    error: str


class HelloWorldNode(BaseModel):
    message: str


class TypeNode(BaseModel):
    id: str
    name: str


class PokemonNode(BaseModel):
    id: str
    no: str
    name: str
    types: List[TypeNode]
    evolutions: Optional[Dict]
