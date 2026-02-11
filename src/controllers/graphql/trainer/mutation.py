# pylint: disable=duplicate-code
from typing import Annotated

import strawberry
from strawberry.types import Info

import usecases.trainer as trainer_ucase
from common.type import UUIDStr
from di.dependency_injection import injector
from di.unit_of_work import AbstractUnitOfWork

from .mapper import TrainerInputMapper, TrainerNodeMapper
from .schema import (
    CatchPokemonInput,
    CreateTrainerInput,
    ReleasePokemonInput,
    TradeNode,
    TradePokemonInput,
    TrainerNode,
    UpdateTrainerInput,
)


@strawberry.type
class TrainerMutation:
    @strawberry.field
    async def create_trainer(
        self,
        input_: Annotated[CreateTrainerInput, strawberry.argument(name='input')],
        _: Info,
    ) -> TrainerNode:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        create_data = TrainerInputMapper.create_input_to_entity(input_)
        created_trainer = await trainer_ucase.create_trainer(async_unit_of_work, create_data)

        return TrainerNodeMapper.entity_to_node(created_trainer)

    @strawberry.field
    async def update_trainer(
        self,
        id: Annotated[str, strawberry.argument(description=UUIDStr.__doc__)],
        input_: Annotated[UpdateTrainerInput, strawberry.argument(name='input')],
        _: Info,
    ) -> TrainerNode:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        id = UUIDStr(id)
        update_data = TrainerInputMapper.update_input_to_entity(input_)
        updated_trainer = await trainer_ucase.update_trainer(async_unit_of_work, id, update_data)

        return TrainerNodeMapper.entity_to_node(updated_trainer)

    @strawberry.field
    async def delete_trainer(
        self,
        id: Annotated[str, strawberry.argument(description=UUIDStr.__doc__)],
        _: Info,
    ) -> None:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        id = UUIDStr(id)
        await trainer_ucase.delete_trainer(async_unit_of_work, id)

    @strawberry.field
    async def catch_pokemon(
        self,
        id: Annotated[str, strawberry.argument(description=UUIDStr.__doc__)],
        input_: Annotated[CatchPokemonInput, strawberry.argument(name='input')],
        _: Info,
    ) -> TrainerNode:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        id = UUIDStr(id)
        catch_data = TrainerInputMapper.catch_input_to_entity(input_)
        trainer = await trainer_ucase.catch_pokemon(async_unit_of_work, id, catch_data)

        return TrainerNodeMapper.entity_to_node(trainer)

    @strawberry.field
    async def release_pokemon(
        self,
        id: Annotated[str, strawberry.argument(description=UUIDStr.__doc__)],
        input_: Annotated[ReleasePokemonInput, strawberry.argument(name='input')],
        _: Info,
    ) -> TrainerNode:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        id = UUIDStr(id)
        release_data = TrainerInputMapper.release_input_to_entity(input_)
        trainer = await trainer_ucase.release_pokemon(async_unit_of_work, id, release_data)

        return TrainerNodeMapper.entity_to_node(trainer)

    @strawberry.field
    async def trade_pokemon(
        self,
        input_: Annotated[TradePokemonInput, strawberry.argument(name='input')],
        _: Info,
    ) -> TradeNode:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        trade_data = TrainerInputMapper.trade_input_to_entity(input_)
        trainer, other_trainer = await trainer_ucase.trade_pokemon(async_unit_of_work, trade_data)

        return TrainerNodeMapper.trade_to_node(trainer, other_trainer)
