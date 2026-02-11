# pylint: disable=duplicate-code
from common.docstring import MAPPER_DOCSTRING
from common.type import PokemonNumberStr, UUIDStr
from models.trainer import (
    CatchPokemonModel,
    CreateTrainerModel,
    ReleasePokemonModel,
    TradePokemonModel,
    TrainerModel,
    TrainerPokemonModel,
    UpdateTrainerModel,
)

from .schema import (
    CatchPokemonInput,
    CreateTrainerInput,
    ReleasePokemonInput,
    TradeNode,
    TradePokemonInput,
    TrainerNode,
    TrainerPokemonNode,
    UpdateTrainerInput,
)

__doc__ = MAPPER_DOCSTRING


class TrainerInputMapper:
    @staticmethod
    def create_input_to_entity(instance: CreateTrainerInput) -> CreateTrainerModel:
        return CreateTrainerModel(
            name=instance.name,
            region=instance.region,
            badge_count=instance.badge_count,
        )

    @staticmethod
    def update_input_to_entity(instance: UpdateTrainerInput) -> UpdateTrainerModel:
        return UpdateTrainerModel(
            name=instance.name,
            region=instance.region,
            badge_count=instance.badge_count,
        )

    @staticmethod
    def catch_input_to_entity(instance: CatchPokemonInput) -> CatchPokemonModel:
        return CatchPokemonModel(pokemon_no=PokemonNumberStr(instance.pokemon_no))

    @staticmethod
    def release_input_to_entity(instance: ReleasePokemonInput) -> ReleasePokemonModel:
        return ReleasePokemonModel(pokemon_no=PokemonNumberStr(instance.pokemon_no))

    @staticmethod
    def trade_input_to_entity(instance: TradePokemonInput) -> TradePokemonModel:
        return TradePokemonModel(
            trainer_id=UUIDStr(instance.trainer_id),
            other_trainer_id=UUIDStr(instance.other_trainer_id),
            pokemon_no=PokemonNumberStr(instance.pokemon_no),
            other_pokemon_no=PokemonNumberStr(instance.other_pokemon_no),
        )


class TrainerNodeMapper:
    @staticmethod
    def entity_to_node(instance: TrainerModel) -> TrainerNode:
        return TrainerNode(
            id=instance.id,
            name=instance.name,
            region=instance.region,
            badge_count=instance.badge_count,
            team=list(map(TrainerPokemonNodeMapper.entity_to_node, instance.team)),
        )

    @staticmethod
    def trade_to_node(trainer: TrainerModel, other_trainer: TrainerModel) -> TradeNode:
        return TradeNode(
            trainer=TrainerNodeMapper.entity_to_node(trainer),
            other_trainer=TrainerNodeMapper.entity_to_node(other_trainer),
        )


class TrainerPokemonNodeMapper:
    @staticmethod
    def entity_to_node(instance: TrainerPokemonModel) -> TrainerPokemonNode:
        return TrainerPokemonNode(no=instance.no, name=instance.name)
