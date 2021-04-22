from typing import List, Optional

from pydantic import BaseModel


class CreatePokemonParams(BaseModel):
    no: str
    name: str
    types: List[str]


class UpdatePokemonParams(BaseModel):
    name: Optional[str]
    types: Optional[List[str]]


class AddEvolutionParams(BaseModel):
    evolutions_no: List[str]


class HTTPBadRequest(BaseModel):
    error: str


class HelloWorldNode(BaseModel):
    message: str


class TypeNode(BaseModel):
    id: str
    name: str


class EvolutionNode(BaseModel):
    class EvolutionPokemonNode(BaseModel):
        id: str
        no: str
        name: str

    before: List[EvolutionPokemonNode]
    after: List[EvolutionPokemonNode]


class PokemonNode(BaseModel):
    id: str
    no: str
    name: str
    types: List[TypeNode]
    evolutions: EvolutionNode
