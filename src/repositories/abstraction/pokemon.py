import abc
from typing import Any, List, Optional

from common.type import PokemonNumberStr
from models.pokemon import (
    CreatePokemonModel,
    GetPokemonParamsModel,
    PokemonModel,
    UpdatePokemonModel,
)


class AbstractPokemonRepository(abc.ABC):
    session: Any

    @abc.abstractmethod
    async def get(self, no: PokemonNumberStr):
        raise NotImplementedError

    @abc.abstractmethod
    async def list(self, params: Optional[GetPokemonParamsModel] = None) -> List[PokemonModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, data: CreatePokemonModel) -> PokemonNumberStr:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, no: PokemonNumberStr, data: UpdatePokemonModel):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, no: PokemonNumberStr):
        raise NotImplementedError

    @abc.abstractmethod
    async def are_existed(self, numbers: List[PokemonNumberStr]) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def replace_types(self, pokemon_no: PokemonNumberStr, type_names: List[str]):
        raise NotImplementedError

    @abc.abstractmethod
    async def replace_previous_evolutions(
        self, pokemon_no: PokemonNumberStr, previous_evolution_numbers: List[PokemonNumberStr]
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def replace_next_evolutions(
        self, pokemon_no: PokemonNumberStr, next_evolution_numbers: List[PokemonNumberStr]
    ):
        raise NotImplementedError
