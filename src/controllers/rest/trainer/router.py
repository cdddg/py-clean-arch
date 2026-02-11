# pylint: disable=duplicate-code
from fastapi import APIRouter, Body, Path, status

from common.type import UUIDStr
from di.dependency_injection import injector
from di.unit_of_work import AbstractUnitOfWork
from usecases import trainer as trainer_ucase

from .mapper import TrainerRequestMapper, TrainerResponseMapper
from .schema import (
    CatchPokemonRequest,
    CreateTrainerRequest,
    ReleasePokemonRequest,
    TradePokemonRequest,
    TradeResponse,
    TrainerResponse,
    UpdateTrainerRequest,
)

router = APIRouter()


@router.post('/trainers', status_code=status.HTTP_201_CREATED)
async def create_trainer(body: CreateTrainerRequest) -> TrainerResponse:
    async_unit_of_work = injector.get(AbstractUnitOfWork)
    create_data = TrainerRequestMapper.create_request_to_entity(body)
    created_trainer = await trainer_ucase.create_trainer(async_unit_of_work, create_data)

    return TrainerResponseMapper.entity_to_response(created_trainer)


@router.get('/trainers/{id}')
async def get_trainer(id: str = Path(..., description=UUIDStr.__doc__)) -> TrainerResponse:
    async_unit_of_work = injector.get(AbstractUnitOfWork)
    id = UUIDStr(id)
    trainer = await trainer_ucase.get_trainer(async_unit_of_work, id)

    return TrainerResponseMapper.entity_to_response(trainer)


@router.get('/trainers')
async def get_trainers() -> list[TrainerResponse]:
    async_unit_of_work = injector.get(AbstractUnitOfWork)
    trainers = await trainer_ucase.get_trainers(async_unit_of_work)

    return list(map(TrainerResponseMapper.entity_to_response, trainers))


@router.patch('/trainers/{id}')
async def update_trainer(
    id: str = Path(..., description=UUIDStr.__doc__),
    body: UpdateTrainerRequest = Body(...),
) -> TrainerResponse:
    async_unit_of_work = injector.get(AbstractUnitOfWork)
    id = UUIDStr(id)
    update_data = TrainerRequestMapper.update_request_to_entity(body)
    updated_trainer = await trainer_ucase.update_trainer(async_unit_of_work, id, update_data)

    return TrainerResponseMapper.entity_to_response(updated_trainer)


@router.delete('/trainers/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_trainer(id: str = Path(..., description=UUIDStr.__doc__)):
    async_unit_of_work = injector.get(AbstractUnitOfWork)
    id = UUIDStr(id)
    await trainer_ucase.delete_trainer(async_unit_of_work, id)


@router.post('/trainers/{id}/catch')
async def catch_pokemon(
    id: str = Path(..., description=UUIDStr.__doc__),
    body: CatchPokemonRequest = Body(...),
) -> TrainerResponse:
    async_unit_of_work = injector.get(AbstractUnitOfWork)
    id = UUIDStr(id)
    catch_data = TrainerRequestMapper.catch_request_to_entity(body)
    trainer = await trainer_ucase.catch_pokemon(async_unit_of_work, id, catch_data)

    return TrainerResponseMapper.entity_to_response(trainer)


@router.post('/trainers/{id}/release')
async def release_pokemon(
    id: str = Path(..., description=UUIDStr.__doc__),
    body: ReleasePokemonRequest = Body(...),
) -> TrainerResponse:
    async_unit_of_work = injector.get(AbstractUnitOfWork)
    id = UUIDStr(id)
    release_data = TrainerRequestMapper.release_request_to_entity(body)
    trainer = await trainer_ucase.release_pokemon(async_unit_of_work, id, release_data)

    return TrainerResponseMapper.entity_to_response(trainer)


@router.post('/trainers/trade')
async def trade_pokemon(body: TradePokemonRequest) -> TradeResponse:
    async_unit_of_work = injector.get(AbstractUnitOfWork)
    trade_data = TrainerRequestMapper.trade_request_to_entity(body)
    trainer, other_trainer = await trainer_ucase.trade_pokemon(async_unit_of_work, trade_data)

    return TrainerResponseMapper.trade_to_response(trainer, other_trainer)
