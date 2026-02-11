from typing import Annotated

import strawberry
from strawberry.types import Info

import usecases.trainer as trainer_ucase
from common.type import UUIDStr
from di.dependency_injection import injector
from di.unit_of_work import AbstractUnitOfWork

from .mapper import TrainerNodeMapper
from .schema import TrainerNode


@strawberry.type
class TrainerQuery:
    @strawberry.field
    async def trainers(self, _: Info) -> list[TrainerNode]:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        trainers = await trainer_ucase.get_trainers(async_unit_of_work)

        return list(map(TrainerNodeMapper.entity_to_node, trainers))

    @strawberry.field
    async def trainer(
        self,
        id: Annotated[str, strawberry.argument(description=UUIDStr.__doc__)],
        _: Info,
    ) -> TrainerNode:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        id = UUIDStr(id)
        trainer = await trainer_ucase.get_trainer(async_unit_of_work, id)

        return TrainerNodeMapper.entity_to_node(trainer)
