from common.docstring import MAPPER_DOCSTRING
from models.pokemon import PokemonEvolutionModel, PokemonModel, TypeModel

from .orm import Pokemon, Type

__doc__ = MAPPER_DOCSTRING


class PokemonOrmMapper:
    @staticmethod
    def orm_to_entity(pokemon: Pokemon) -> PokemonModel:
        return PokemonModel(
            no=pokemon.no,
            name=pokemon.name,
            types=list(map(TypeOrmMapper.orm_to_entity, pokemon.types)),
            previous_evolutions=[
                PokemonEvolutionModel(
                    no=evo.previous_pokemon.no,
                    name=evo.previous_pokemon.name,
                )
                for evo in pokemon.previous_evolutions
                if evo.previous_pokemon
            ],
            next_evolutions=[
                PokemonEvolutionModel(
                    no=evo.next_pokemon.no,
                    name=evo.next_pokemon.name,
                )
                for evo in pokemon.next_evolutions
                if evo.next_pokemon
            ],
        )


class TypeOrmMapper:
    @staticmethod
    def orm_to_entity(type_: Type) -> TypeModel:
        return TypeModel(id=type_.id, name=type_.name)
