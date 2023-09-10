from models.pokemon import PokemonEvolutionModel, PokemonModel, TypeModel

from .orm import Pokemon, Type


class PokemonOrmMapper:
    @staticmethod
    def orm_to_entity(pokemon: Pokemon) -> PokemonModel:
        return PokemonModel(
            no=pokemon.no,
            name=pokemon.name,
            types=list(map(TypeOrmMapper.orm_to_entity, pokemon.types)),
            before_evolutions=[
                PokemonEvolutionModel(
                    no=evo.before_pokemon.no,
                    name=evo.before_pokemon.name,
                )
                for evo in pokemon.before_evolutions
                if evo.before_pokemon
            ],
            after_evolutions=[
                PokemonEvolutionModel(
                    no=evo.after_pokemon.no,
                    name=evo.after_pokemon.name,
                )
                for evo in pokemon.after_evolutions
                if evo.after_pokemon
            ],
        )


class TypeOrmMapper:
    @staticmethod
    def orm_to_entity(type_: Type) -> TypeModel:
        return TypeModel(id=type_.id, name=type_.name)
