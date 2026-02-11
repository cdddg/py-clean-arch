from common.docstring import MAPPER_DOCSTRING
from models.trainer import TrainerModel, TrainerPokemonModel

__doc__ = MAPPER_DOCSTRING


class TrainerKeyValueMapper:
    @staticmethod
    def dict_to_entity(key_value: dict) -> TrainerModel:
        return TrainerModel(
            id=key_value['id'],
            name=key_value['name'],
            region=key_value['region'],
            badge_count=int(key_value['badge_count']),
            team=[
                TrainerPokemonModel(no=p['no'], name=p['name']) for p in key_value.get('team', [])
            ],
        )
