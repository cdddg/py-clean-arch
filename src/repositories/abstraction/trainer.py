# pylint: disable=duplicate-code
import abc
from typing import Any, List

from common.type import PokemonNumberStr, UUIDStr
from models.trainer import (
    CreateTrainerModel,
    TrainerModel,
    UpdateTrainerModel,
)


class AbstractTrainerRepository(abc.ABC):
    session: Any

    @abc.abstractmethod
    async def get(self, id: UUIDStr) -> TrainerModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def list(self) -> List[TrainerModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, data: CreateTrainerModel) -> UUIDStr:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, id: UUIDStr, data: UpdateTrainerModel):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, id: UUIDStr):
        raise NotImplementedError

    @abc.abstractmethod
    async def add_to_team(self, trainer_id: UUIDStr, pokemon_no: PokemonNumberStr):
        raise NotImplementedError

    @abc.abstractmethod
    async def remove_from_team(self, trainer_id: UUIDStr, pokemon_no: PokemonNumberStr):
        raise NotImplementedError

    @abc.abstractmethod
    async def remove_pokemon_from_all_teams(self, pokemon_no: PokemonNumberStr):
        raise NotImplementedError
