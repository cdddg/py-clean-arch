from typing import Optional, Union

import strawberry
from strawberry.exceptions import GraphQLError
from strawberry.types import ExecutionContext
from strawberry.utils.logging import StrawberryLogger

from models.pokemon import (
    CreatePokemonModel,
    PokemonEvolutionModel,
    PokemonModel,
    TypeModel,
    UpdatePokemonModel,
)
from settings import IS_TEST

from .scalar import UUIDStrScalar


class Schema(strawberry.Schema):
    def process_errors(
        self,
        errors: list[GraphQLError],
        execution_context: Optional[ExecutionContext] = None,
    ):
        # https://github.com/strawberry-graphql/strawberry/issues/847
        # https://github.com/strawberry-graphql/strawberry/pull/851

        for error in errors:
            _error: Union[Exception, GraphQLError] = error
            if isinstance(error, GraphQLError) and error.original_error:
                _error = error.original_error
            if IS_TEST or 1:
                raise _error

            error.message = f'{type(_error).__name__}: {error.message}'
            StrawberryLogger.error(error, execution_context)


@strawberry.input
class CreatePokemonInput:
    no: str
    name: str
    type_names: list[str]
    before_evolution_numbers: Optional[list[str]] = None
    after_evolution_numbers: Optional[list[str]] = None

    def to_instance(self) -> CreatePokemonModel:
        return CreatePokemonModel(
            no=self.no,
            name=self.name,
            type_names=self.type_names,
            before_evolution_numbers=self.before_evolution_numbers or [],
            after_evolution_numbers=self.after_evolution_numbers or [],
        )


@strawberry.input
class UpdatePokemonInput:
    name: Optional[str] = None
    type_names: Optional[list[str]] = None
    before_evolution_numbers: Optional[list[str]] = None
    after_evolution_numbers: Optional[list[str]] = None

    def to_instance(self) -> UpdatePokemonModel:
        return UpdatePokemonModel(
            name=self.name,
            type_names=self.type_names,
            before_evolution_numbers=self.before_evolution_numbers,
            after_evolution_numbers=self.after_evolution_numbers,
        )


@strawberry.type
class TypeNode:
    id: UUIDStrScalar
    name: str

    @classmethod
    def from_instance(cls, instance: TypeModel) -> 'TypeNode':
        return cls(id=instance.id, name=instance.name)  # pyright: ignore[reportGeneralTypeIssues]


@strawberry.type
class EvolutionNode:
    no: str
    name: str

    @classmethod
    def from_instance(cls, instance: PokemonEvolutionModel) -> 'EvolutionNode':
        return cls(no=instance.no, name=instance.name)


@strawberry.type
class PokemonNode:
    no: str
    name: str
    types: list[TypeNode]
    before_evolutions: list[EvolutionNode]
    after_evolutions: list[EvolutionNode]

    @classmethod
    def from_instance(cls, instance: PokemonModel) -> 'PokemonNode':
        return cls(
            no=instance.no,
            name=instance.name,
            types=list(map(TypeNode.from_instance, instance.types)),
            before_evolutions=list(map(EvolutionNode.from_instance, instance.before_evolutions)),
            after_evolutions=list(map(EvolutionNode.from_instance, instance.after_evolutions)),
        )
