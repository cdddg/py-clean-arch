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
    CatchPokemonRequest,
    CreateTrainerRequest,
    ReleasePokemonRequest,
    TradePokemonRequest,
    TradeResponse,
    TrainerPokemonResponse,
    TrainerResponse,
    UpdateTrainerRequest,
)

__doc__ = MAPPER_DOCSTRING


class TrainerRequestMapper:
    @staticmethod
    def create_request_to_entity(instance: CreateTrainerRequest) -> CreateTrainerModel:
        return CreateTrainerModel(
            name=instance.name,
            region=instance.region,
            badge_count=instance.badge_count,
        )

    @staticmethod
    def update_request_to_entity(instance: UpdateTrainerRequest) -> UpdateTrainerModel:
        return UpdateTrainerModel(**instance.model_dump(exclude_unset=True))

    @staticmethod
    def catch_request_to_entity(instance: CatchPokemonRequest) -> CatchPokemonModel:
        return CatchPokemonModel(pokemon_no=PokemonNumberStr(instance.pokemon_no))

    @staticmethod
    def release_request_to_entity(instance: ReleasePokemonRequest) -> ReleasePokemonModel:
        return ReleasePokemonModel(pokemon_no=PokemonNumberStr(instance.pokemon_no))

    @staticmethod
    def trade_request_to_entity(instance: TradePokemonRequest) -> TradePokemonModel:
        return TradePokemonModel(
            trainer_id=UUIDStr(instance.trainer_id),
            other_trainer_id=UUIDStr(instance.other_trainer_id),
            pokemon_no=PokemonNumberStr(instance.pokemon_no),
            other_pokemon_no=PokemonNumberStr(instance.other_pokemon_no),
        )


class TrainerResponseMapper:
    @staticmethod
    def entity_to_response(instance: TrainerModel) -> TrainerResponse:
        return TrainerResponse(
            id=instance.id,
            name=instance.name,
            region=instance.region,
            badge_count=instance.badge_count,
            team=list(map(TrainerPokemonResponseMapper.entity_to_response, instance.team)),
        )

    @staticmethod
    def trade_to_response(trainer: TrainerModel, other_trainer: TrainerModel) -> TradeResponse:
        return TradeResponse(
            trainer=TrainerResponseMapper.entity_to_response(trainer),
            other_trainer=TrainerResponseMapper.entity_to_response(other_trainer),
        )


class TrainerPokemonResponseMapper:
    @staticmethod
    def entity_to_response(instance: TrainerPokemonModel) -> TrainerPokemonResponse:
        return TrainerPokemonResponse(no=instance.no, name=instance.name)
