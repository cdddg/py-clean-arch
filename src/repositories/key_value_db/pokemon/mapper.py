import uuid

from common.type import UUIDStr
from models.pokemon import PokemonEvolutionModel, PokemonModel, TypeModel


class PokemonKeyValueMapper:
    @staticmethod
    def dict_to_entity(key_value: dict) -> PokemonModel:
        return PokemonModel(
            no=key_value['no'],
            name=key_value['name'],
            types=[
                TypeModel(id=UUIDStr(uuid.uuid5(uuid.NAMESPACE_DNS, name).hex), name=name)
                for name in key_value['types']
            ],
            previous_evolutions=[
                PokemonEvolutionModel(no=evo['no'], name=evo['name'])
                for evo in key_value['previous_evolutions'] or []
            ],
            next_evolutions=[
                PokemonEvolutionModel(no=evo['no'], name=evo['name'])
                for evo in key_value['next_evolutions'] or []
            ],
        )
