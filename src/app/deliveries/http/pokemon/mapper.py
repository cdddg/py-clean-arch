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


class PokemonRequestMapper:
    @staticmethod
    def create_request_to_entity(request: CreatePokemonRequest) -> CreatePokemonModel:
        return CreatePokemonModel(
            no=PokemonNumberStr(request.no),
            name=request.name,
            type_names=request.type_names or [],
            before_evolution_numbers=list(
                map(PokemonNumberStr, request.before_evolution_numbers or [])
            ),
            after_evolution_numbers=list(
                map(PokemonNumberStr, request.after_evolution_numbers or [])
            ),
        )

    @staticmethod
    def update_request_to_entity(request: UpdatePokemonRequest) -> UpdatePokemonModel:
        kwargs = request.dict(exclude_unset=True)
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
