from common.docstring import MAPPER_DOCSTRING
from models.trainer import TrainerModel, TrainerPokemonModel

__doc__ = MAPPER_DOCSTRING


class TrainerDictMapper:
    @staticmethod
    def dict_to_entity(document: dict) -> TrainerModel:
        return TrainerModel(
            id=document['id'],
            name=document['name'],
            region=document['region'],
            badge_count=document['badge_count'],
            team=[
                TrainerPokemonModel(no=p['no'], name=p['name'])
                for p in document.get('team_details', [])
            ],
        )
