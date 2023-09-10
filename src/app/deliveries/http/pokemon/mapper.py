from common.docstring import MAPPER_DOCSTRING
from common.type import PokemonNumberStr
from models.pokemon import (
    CreatePokemonModel,
    PokemonEvolutionModel,
    PokemonModel,
    TypeModel,
    UpdatePokemonModel,
)

from .schema import (
    CreatePokemonRequest,
    EvolutionResponse,
    PokemonResponse,
    TypeResponse,
    UpdatePokemonRequest,
)

__doc__ = MAPPER_DOCSTRING


class PokemonRequestMapper:
    @staticmethod
    def create_request_to_entity(instance: CreatePokemonRequest) -> CreatePokemonModel:
        return CreatePokemonModel(
            no=PokemonNumberStr(instance.no),
            name=instance.name,
            type_names=instance.type_names or [],
            before_evolution_numbers=list(
                map(PokemonNumberStr, instance.before_evolution_numbers or [])
            ),
            after_evolution_numbers=list(
                map(PokemonNumberStr, instance.after_evolution_numbers or [])
            ),
        )

    @staticmethod
    def update_request_to_entity(instance: UpdatePokemonRequest) -> UpdatePokemonModel:
        if instance.before_evolution_numbers:
            instance.before_evolution_numbers = list(
                map(PokemonNumberStr, instance.before_evolution_numbers)
            )
        if instance.after_evolution_numbers:
            instance.after_evolution_numbers = list(
                map(PokemonNumberStr, instance.after_evolution_numbers)
            )
        kwargs = instance.dict(exclude_unset=True)

        return UpdatePokemonModel(**kwargs)


class PokemonResponseMapper:
    @staticmethod
    def entity_to_response(instance: PokemonModel) -> PokemonResponse:
        return PokemonResponse(
            no=instance.no,
            name=instance.name,
            types=list(map(TypeResponseMapper.entity_to_response, instance.types)),
            before_evolutions=list(
                map(EvolutionResponseMapper.entity_to_response, instance.before_evolutions)
            ),
            after_evolutions=list(
                map(EvolutionResponseMapper.entity_to_response, instance.after_evolutions)
            ),
        )


class TypeResponseMapper:
    @staticmethod
    def entity_to_response(instance: TypeModel) -> TypeResponse:
        return TypeResponse(id=instance.id, name=instance.name)


class EvolutionResponseMapper:
    @staticmethod
    def entity_to_response(instance: PokemonEvolutionModel) -> EvolutionResponse:
        return EvolutionResponse(no=instance.no, name=instance.name)
