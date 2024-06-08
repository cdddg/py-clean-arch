import uuid

from common.type import UUIDStr
from models.pokemon import PokemonEvolutionModel, PokemonModel, TypeModel


class PokemonDictMapper:
    @staticmethod
    def dict_to_entity(document: dict) -> PokemonModel:
        return PokemonModel(
            no=document['no'],
            name=document['name'],
            types=[
                TypeModel(id=UUIDStr(uuid.uuid5(uuid.NAMESPACE_DNS, name).hex), name=name)
                for name in document['types']
            ],
            previous_evolutions=[
                PokemonEvolutionModel(no=evo['no'], name=evo['name'])
                for evo in document.get('previous_evolution_details', [])
            ],
            next_evolutions=[
                PokemonEvolutionModel(no=evo['no'], name=evo['name'])
                for evo in document.get('next_evolution_details', [])
            ],
        )
