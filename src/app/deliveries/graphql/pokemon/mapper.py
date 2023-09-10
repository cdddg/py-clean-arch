from common.type import PokemonNumberStr
from models.pokemon import (
    CreatePokemonModel,
    PokemonEvolutionModel,
    PokemonModel,
    TypeModel,
    UpdatePokemonModel,
)

from .schema import CreatePokemonInput, EvolutionNode, PokemonNode, TypeNode, UpdatePokemonInput


class PokemonInputMapper:
    @staticmethod
    def create_input_to_entity(input_data: CreatePokemonInput) -> CreatePokemonModel:
        return CreatePokemonModel(
            no=PokemonNumberStr(input_data.no),
            name=input_data.name,
            type_names=input_data.type_names,
            before_evolution_numbers=list(
                map(PokemonNumberStr, input_data.before_evolution_numbers or [])
            ),
            after_evolution_numbers=list(
                map(PokemonNumberStr, input_data.after_evolution_numbers or [])
            ),
        )

    @staticmethod
    def update_input_to_entity(input_data: UpdatePokemonInput) -> UpdatePokemonModel:
        return UpdatePokemonModel(
            name=input_data.name,
            type_names=input_data.type_names,
            before_evolution_numbers=list(
                map(PokemonNumberStr, input_data.before_evolution_numbers)
            )
            if input_data.before_evolution_numbers is not None
            else None,
            after_evolution_numbers=list(map(PokemonNumberStr, input_data.after_evolution_numbers))
            if input_data.after_evolution_numbers is not None
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
