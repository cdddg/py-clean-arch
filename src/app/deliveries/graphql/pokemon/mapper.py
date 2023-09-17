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
            previous_evolution_numbers=list(
                map(PokemonNumberStr, instance.previous_evolution_numbers or [])
            ),
            next_evolution_numbers=list(
                map(PokemonNumberStr, instance.next_evolution_numbers or [])
            ),
        )

    @staticmethod
    def update_input_to_entity(instance: UpdatePokemonInput) -> UpdatePokemonModel:
        return UpdatePokemonModel(
            name=instance.name,
            type_names=instance.type_names,
            previous_evolution_numbers=list(
                map(PokemonNumberStr, instance.previous_evolution_numbers)
            )
            if instance.previous_evolution_numbers is not None
            else None,
            next_evolution_numbers=list(map(PokemonNumberStr, instance.next_evolution_numbers))
            if instance.next_evolution_numbers is not None
            else None,
        )


class PokemonNodeMapper:
    @staticmethod
    def entity_to_node(instance: PokemonModel) -> PokemonNode:
        return PokemonNode(
            no=instance.no,
            name=instance.name,
            types=list(map(TypeNodeMapper.entity_to_node, instance.types)),
            previous_evolutions=list(
                map(EvolutionNodeMapper.entity_to_node, instance.previous_evolutions)
            ),
            next_evolutions=list(map(EvolutionNodeMapper.entity_to_node, instance.next_evolutions)),
        )


class TypeNodeMapper:
    @staticmethod
    def entity_to_node(instance: TypeModel) -> TypeNode:
        return TypeNode(id=instance.id, name=instance.name)


class EvolutionNodeMapper:
    @staticmethod
    def entity_to_node(instance: PokemonEvolutionModel) -> EvolutionNode:
        return EvolutionNode(no=instance.no, name=instance.name)
