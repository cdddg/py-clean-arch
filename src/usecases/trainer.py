from common.type import UUIDStr
from di.unit_of_work import AbstractUnitOfWork
from models.exception import (
    TrainerAlreadyOwnsPokemon,
    TrainerDoesNotOwnPokemon,
    TrainerTeamFullError,
)
from models.trainer import (
    CatchPokemonModel,
    CreateTrainerModel,
    ReleasePokemonModel,
    TradePokemonModel,
    TrainerModel,
    UpdateTrainerModel,
)


async def create_trainer(
    async_unit_of_work: AbstractUnitOfWork, data: CreateTrainerModel
) -> TrainerModel:
    async with async_unit_of_work as auow:
        id = await auow.trainer_repo.create(data)
        return await auow.trainer_repo.get(id)


async def get_trainer(async_unit_of_work: AbstractUnitOfWork, id: UUIDStr) -> TrainerModel:
    async with async_unit_of_work as auow:
        return await auow.trainer_repo.get(id)


async def get_trainers(async_unit_of_work: AbstractUnitOfWork) -> list[TrainerModel]:
    async with async_unit_of_work as auow:
        return await auow.trainer_repo.list()


async def update_trainer(
    async_unit_of_work: AbstractUnitOfWork, id: UUIDStr, data: UpdateTrainerModel
) -> TrainerModel:
    async with async_unit_of_work as auow:
        await auow.trainer_repo.update(id, data)
        return await auow.trainer_repo.get(id)


async def delete_trainer(async_unit_of_work: AbstractUnitOfWork, id: UUIDStr) -> None:
    async with async_unit_of_work as auow:
        await auow.trainer_repo.delete(id)


async def catch_pokemon(
    async_unit_of_work: AbstractUnitOfWork, trainer_id: UUIDStr, data: CatchPokemonModel
) -> TrainerModel:
    async with async_unit_of_work as auow:
        trainer = await auow.trainer_repo.get(trainer_id)
        await auow.pokemon_repo.get(data.pokemon_no)

        if trainer.is_team_full:
            raise TrainerTeamFullError(f'Trainer {trainer_id} team is full')

        if trainer.has_pokemon(data.pokemon_no):
            raise TrainerAlreadyOwnsPokemon(
                f'Trainer {trainer_id} already owns Pokemon {data.pokemon_no}'
            )

        await auow.trainer_repo.add_to_team(trainer_id, data.pokemon_no)
        return await auow.trainer_repo.get(trainer_id)


async def release_pokemon(
    async_unit_of_work: AbstractUnitOfWork, trainer_id: UUIDStr, data: ReleasePokemonModel
) -> TrainerModel:
    async with async_unit_of_work as auow:
        trainer = await auow.trainer_repo.get(trainer_id)

        if not trainer.has_pokemon(data.pokemon_no):
            raise TrainerDoesNotOwnPokemon(
                f'Trainer {trainer_id} does not own Pokemon {data.pokemon_no}'
            )

        await auow.trainer_repo.remove_from_team(trainer_id, data.pokemon_no)
        return await auow.trainer_repo.get(trainer_id)


async def trade_pokemon(
    async_unit_of_work: AbstractUnitOfWork, data: TradePokemonModel
) -> tuple[TrainerModel, TrainerModel]:
    async with async_unit_of_work as auow:
        trainer = await auow.trainer_repo.get(data.trainer_id)
        other_trainer = await auow.trainer_repo.get(data.other_trainer_id)

        if not trainer.has_pokemon(data.pokemon_no):
            raise TrainerDoesNotOwnPokemon(
                f'Trainer {data.trainer_id} does not own Pokemon {data.pokemon_no}'
            )

        if not other_trainer.has_pokemon(data.other_pokemon_no):
            raise TrainerDoesNotOwnPokemon(
                f'Trainer {data.other_trainer_id} does not own Pokemon {data.other_pokemon_no}'
            )

        if trainer.has_pokemon(data.other_pokemon_no):
            raise TrainerAlreadyOwnsPokemon(
                f'Trainer {data.trainer_id} already owns Pokemon {data.other_pokemon_no}'
            )

        if other_trainer.has_pokemon(data.pokemon_no):
            raise TrainerAlreadyOwnsPokemon(
                f'Trainer {data.other_trainer_id} already owns Pokemon {data.pokemon_no}'
            )

        await auow.trainer_repo.remove_from_team(data.trainer_id, data.pokemon_no)
        await auow.trainer_repo.remove_from_team(data.other_trainer_id, data.other_pokemon_no)
        await auow.trainer_repo.add_to_team(data.trainer_id, data.other_pokemon_no)
        await auow.trainer_repo.add_to_team(data.other_trainer_id, data.pokemon_no)

        return (
            await auow.trainer_repo.get(data.trainer_id),
            await auow.trainer_repo.get(data.other_trainer_id),
        )
