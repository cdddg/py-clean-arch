from common.docstring import MAPPER_DOCSTRING
from common.type import PokemonNumberStr
from models.pokemon import (
    CreatePokemonModel,
    PokemonEvolutionModel,
    PokemonModel,
    TypeModel,
    UpdatePokemonModel,
)

from .schema import CreatePokemonInput, EvolutionNode, PokemonNode, TypeNode, UpdatePokemonInput

__doc__ = MAPPER_DOCSTRING


class PokemonInputMapper:
    @staticmethod
    def create_input_to_entity(instance: CreatePokemonInput) -> CreatePokemonModel:
        return CreatePokemonModel(
            no=PokemonNumberStr(instance.no),
            name=instance.name,
            type_names=instance.type_names,
            before_evolution_numbers=list(
                map(PokemonNumberStr, instance.before_evolution_numbers or [])
            ),
            after_evolution_numbers=list(
                map(PokemonNumberStr, instance.after_evolution_numbers or [])
            ),
        )

    @staticmethod
    def update_input_to_entity(instance: UpdatePokemonInput) -> UpdatePokemonModel:
        return UpdatePokemonModel(
            name=instance.name,
            type_names=instance.type_names,
            before_evolution_numbers=list(map(PokemonNumberStr, instance.before_evolution_numbers))
            if instance.before_evolution_numbers is not None
            else None,
            after_evolution_numbers=list(map(PokemonNumberStr, instance.after_evolution_numbers))
            if instance.after_evolution_numbers is not None
            else None,
        )


class PokemonNodeMapper:
    @staticmethod
    def entity_to_node(instance: PokemonModel) -> PokemonNode:
        return PokemonNode(
            no=instance.no,
            name=instance.name,
            types=list(map(TypeNodeMapper.entity_to_node, instance.types)),
            before_evolutions=list(
                map(EvolutionNodeMapper.entity_to_node, instance.before_evolutions)
            ),
            after_evolutions=list(
                map(EvolutionNodeMapper.entity_to_node, instance.after_evolutions)
            ),
        )


class TypeNodeMapper:
    @staticmethod
    def entity_to_node(instance: TypeModel) -> TypeNode:
        return TypeNode(id=instance.id, name=instance.name)


class EvolutionNodeMapper:
    @staticmethod
    def entity_to_node(instance: PokemonEvolutionModel) -> EvolutionNode:
        return EvolutionNode(no=instance.no, name=instance.name)
