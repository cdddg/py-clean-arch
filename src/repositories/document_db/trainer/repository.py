# pylint: disable=duplicate-code
from typing import List

from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorCollection

from common.type import PokemonNumberStr, UUIDStr
from common.utils import build_uuid4_str
from models.exception import TrainerNotFound
from models.trainer import (
    CreateTrainerModel,
    TrainerModel,
    UpdateTrainerModel,
)

from ...abstraction import AbstractTrainerRepository
from .mapper import TrainerDictMapper

POKEMON_COLLECTION_NAME = 'pokemon'


class MongoDBTrainerRepository(AbstractTrainerRepository):
    LOOKUP = '$lookup'
    UNWIND = '$unwind'
    SORT = '$sort'
    GROUP = '$group'
    FIRST = '$first'
    PUSH = '$push'
    MATCH = '$match'
    SET = '$set'

    # fmt: off
    def __init__(
        self,
        collection: AsyncIOMotorCollection,  # pyright: ignore[reportInvalidTypeForm]
        pokemon_collection: AsyncIOMotorCollection,  # pyright: ignore[reportInvalidTypeForm]
        session: AsyncIOMotorClientSession | None = None,  # pyright: ignore[reportInvalidTypeForm]
    ):
        self.collection = collection
        self.pokemon_collection = pokemon_collection
        self.session = session
    # fmt: on

    def _build_team_pipeline(self) -> List:
        return [
            {
                self.LOOKUP: {
                    'from': POKEMON_COLLECTION_NAME,
                    'localField': 'team',
                    'foreignField': 'no',
                    'as': 'team_details',
                }
            },
            {self.SORT: {'id': 1}},
        ]

    async def get(self, id: UUIDStr) -> TrainerModel:
        pipeline = self._build_team_pipeline()
        pipeline.insert(0, {self.MATCH: {'id': id}})
        try:
            document = await self.collection.aggregate(pipeline, session=self.session).next()
            if not document:
                raise TrainerNotFound(id)
        except StopAsyncIteration:
            raise TrainerNotFound(id)

        return TrainerDictMapper.dict_to_entity(document)

    async def list(self) -> List[TrainerModel]:
        pipeline = self._build_team_pipeline()
        cursor = self.collection.aggregate(pipeline, session=self.session)
        documents = await cursor.to_list(None)

        return list(map(TrainerDictMapper.dict_to_entity, documents))

    async def create(self, data: CreateTrainerModel) -> UUIDStr:
        id = UUIDStr(build_uuid4_str())
        document = {
            'id': id,
            'name': data.name,
            'region': data.region,
            'badge_count': data.badge_count,
            'team': [],
        }
        await self.collection.insert_one(document, session=self.session)

        return id

    async def update(self, id: UUIDStr, data: UpdateTrainerModel):
        values = {}
        if data.name is not None:
            values['name'] = data.name
        if data.region is not None:
            values['region'] = data.region
        if data.badge_count is not None:
            values['badge_count'] = data.badge_count

        if values:
            result = await self.collection.update_one(
                {'id': id},
                {self.SET: values},
                session=self.session,
            )
            if result.matched_count == 0:
                raise TrainerNotFound(id)

    async def delete(self, id: UUIDStr):
        result = await self.collection.delete_one({'id': id}, session=self.session)
        if result.deleted_count == 0:
            raise TrainerNotFound(id)

    async def add_to_team(self, trainer_id: UUIDStr, pokemon_no: PokemonNumberStr):
        await self.collection.update_one(
            {'id': trainer_id},
            {self.PUSH: {'team': pokemon_no}},
            session=self.session,
        )

    async def remove_from_team(self, trainer_id: UUIDStr, pokemon_no: PokemonNumberStr):
        await self.collection.update_one(
            {'id': trainer_id},
            {'$pull': {'team': pokemon_no}},
            session=self.session,
        )

    async def remove_pokemon_from_all_teams(self, pokemon_no: PokemonNumberStr):
        await self.collection.update_many(
            {'team': pokemon_no},
            {'$pull': {'team': pokemon_no}},
            session=self.session,
        )
