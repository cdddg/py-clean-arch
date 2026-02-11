# pylint: disable=duplicate-code
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import delete, insert, select, update

from common.type import PokemonNumberStr, UUIDStr
from models.exception import TrainerNotFound
from models.trainer import (
    CreateTrainerModel,
    TrainerModel,
    UpdateTrainerModel,
)

from ...abstraction import AbstractTrainerRepository
from .mapper import TrainerOrmMapper
from .orm import Trainer, TrainerPokemon


class RelationalDBTrainerRepository(AbstractTrainerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _select_with_team(self):
        return select(Trainer).options(
            selectinload(Trainer.team).joinedload(TrainerPokemon.pokemon)
        )

    async def get(self, id: UUIDStr) -> TrainerModel:
        stmt = self._select_with_team().where(Trainer.id == id)
        trainer = (await self.session.execute(stmt)).scalars().one_or_none()
        if not trainer:
            raise TrainerNotFound(id)

        return TrainerOrmMapper.orm_to_entity(trainer)

    async def list(self) -> List[TrainerModel]:
        stmt = self._select_with_team()
        trainers = (await self.session.execute(stmt)).scalars().unique().all()

        return list(map(TrainerOrmMapper.orm_to_entity, trainers))

    async def create(self, data: CreateTrainerModel) -> UUIDStr:
        trainer = Trainer(
            name=data.name,
            region=data.region,
            badge_count=data.badge_count,
        )
        self.session.add(trainer)
        await self.session.flush()

        return trainer.id

    async def update(self, id: UUIDStr, data: UpdateTrainerModel):
        values = {}
        if data.name is not None:
            values['name'] = data.name
        if data.region is not None:
            values['region'] = data.region
        if data.badge_count is not None:
            values['badge_count'] = data.badge_count

        if values:
            stmt = update(Trainer).where(Trainer.id == id).values(**values)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                raise TrainerNotFound(id)

    async def delete(self, id: UUIDStr):
        stmt = delete(Trainer).where(Trainer.id == id)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise TrainerNotFound(id)

    async def add_to_team(self, trainer_id: UUIDStr, pokemon_no: PokemonNumberStr):
        stmt = insert(TrainerPokemon).values(trainer_id=trainer_id, pokemon_no=pokemon_no)
        await self.session.execute(stmt)

    async def remove_from_team(self, trainer_id: UUIDStr, pokemon_no: PokemonNumberStr):
        stmt = delete(TrainerPokemon).where(
            TrainerPokemon.trainer_id == trainer_id,
            TrainerPokemon.pokemon_no == pokemon_no,
        )
        await self.session.execute(stmt)

    async def remove_pokemon_from_all_teams(self, pokemon_no: PokemonNumberStr):
        stmt = delete(TrainerPokemon).where(TrainerPokemon.pokemon_no == pokemon_no)
        await self.session.execute(stmt)
