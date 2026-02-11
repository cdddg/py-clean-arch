from common.docstring import MAPPER_DOCSTRING
from models.trainer import TrainerModel, TrainerPokemonModel

from .orm import Trainer

__doc__ = MAPPER_DOCSTRING


class TrainerOrmMapper:
    @staticmethod
    def orm_to_entity(trainer: Trainer) -> TrainerModel:
        return TrainerModel(
            id=trainer.id,
            name=trainer.name,
            region=trainer.region,
            badge_count=trainer.badge_count,
            team=[
                TrainerPokemonModel(
                    no=tp.pokemon.no,
                    name=tp.pokemon.name,
                )
                for tp in trainer.team
                if tp.pokemon
            ],
        )
