from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorCollection

from common.type import PokemonNumberStr
from models.exception import PokemonAlreadyExists, PokemonNotFound
from models.pokemon import (
    CreatePokemonModel,
    GetPokemonParamsModel,
    PokemonModel,
    UpdatePokemonModel,
)

from ...abstraction import AbstractPokemonRepository
from .mapper import PokemonDictMapper


class MongoDBPokemonRepository(AbstractPokemonRepository):
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
        session: Optional[AsyncIOMotorClientSession] = None,  # pyright: ignore[reportInvalidTypeForm]
    ):
        self.collection = collection
        self.session = session
    # fmt: on

    def _build_evolution_pipeline(self) -> List:
        PREVIOUS_EVOLUTION_DETAILS = 'previous_evolution_details'
        NEXT_EVOLUTION_DETAILS = 'next_evolution_details'

        return [
            # previous_evolutions
            {
                self.LOOKUP: {
                    'from': self.collection.name,
                    'localField': 'previous_evolution_object_ids',
                    'foreignField': '_id',
                    'as': PREVIOUS_EVOLUTION_DETAILS,
                }
            },
            {
                self.UNWIND: {
                    'path': f'${PREVIOUS_EVOLUTION_DETAILS}',
                    'preserveNullAndEmptyArrays': True,
                }
            },
            {self.SORT: {f'{PREVIOUS_EVOLUTION_DETAILS}.no': 1}},
            {
                self.GROUP: {
                    '_id': '$_id',
                    'no': {self.FIRST: '$no'},
                    'name': {self.FIRST: '$name'},
                    'types': {self.FIRST: '$types'},
                    'previous_evolution_object_ids': {self.FIRST: '$previous_evolution_object_ids'},
                    'next_evolution_object_ids': {self.FIRST: '$next_evolution_object_ids'},
                    PREVIOUS_EVOLUTION_DETAILS: {self.PUSH: f'${PREVIOUS_EVOLUTION_DETAILS}'},
                }
            },
            # next_evolution_object_ids
            {
                self.LOOKUP: {
                    'from': self.collection.name,
                    'localField': 'next_evolution_object_ids',
                    'foreignField': '_id',
                    'as': NEXT_EVOLUTION_DETAILS,
                }
            },
            {
                self.UNWIND: {
                    'path': f'${NEXT_EVOLUTION_DETAILS}',
                    'preserveNullAndEmptyArrays': True,
                }
            },
            {self.SORT: {f'{NEXT_EVOLUTION_DETAILS}.no': 1}},
            {
                self.GROUP: {
                    '_id': '$_id',
                    'no': {self.FIRST: '$no'},
                    'name': {self.FIRST: '$name'},
                    'types': {self.FIRST: '$types'},
                    'previous_evolution_object_ids': {self.FIRST: '$previous_evolution_object_ids'},
                    PREVIOUS_EVOLUTION_DETAILS: {self.FIRST: f'${PREVIOUS_EVOLUTION_DETAILS}'},
                    'next_evolution_object_ids': {self.FIRST: '$next_evolution_object_ids'},
                    NEXT_EVOLUTION_DETAILS: {self.PUSH: f'${NEXT_EVOLUTION_DETAILS}'},
                }
            },
        ]

    async def _get_filtered_pokemon_id_map(
        self, numbers: List[PokemonNumberStr]
    ) -> dict[PokemonNumberStr, ObjectId]:
        cursor = self.collection.find({'no': {'$in': numbers}}, session=self.session)

        return {
            document['no']: document['_id']
            for document in await cursor.to_list(None)  # pyright: ignore[reportGeneralTypeIssues]
        }

    async def get(self, no: PokemonNumberStr):
        pipeline = self._build_evolution_pipeline()
        pipeline.append({self.MATCH: {'no': no}})
        try:
            document = await self.collection.aggregate(pipeline, session=self.session).next()
            if not document:
                raise PokemonNotFound(no)
        except StopAsyncIteration:
            raise PokemonNotFound(no)

        return PokemonDictMapper.dict_to_entity(document)

    async def list(self, params: Optional[GetPokemonParamsModel] = None) -> List[PokemonModel]:
        pipeline = self._build_evolution_pipeline()
        pipeline.append({self.SORT: {'no': 1}})
        if params:
            pipeline.append({'$skip': (params.page - 1) * params.size})
            pipeline.append({'$limit': params.size})
        cursor = self.collection.aggregate(pipeline, session=self.session)
        documents = await cursor.to_list(None)

        return list(map(PokemonDictMapper.dict_to_entity, documents))

    async def create(self, data: CreatePokemonModel) -> PokemonNumberStr:
        count = await self.collection.count_documents(
            {'no': data.no},
            session=self.session,
        )
        if count > 0:
            raise PokemonAlreadyExists(data.no)

        document = {
            'no': data.no,
            'name': data.name,
            'hp': None,
            'attack': None,
            'defense': None,
            'sp_atk': None,
            'sp_def': None,
            'speed': None,
            'types': [],
            'previous_evolution_object_ids': [],
            'next_evolution_object_ids': [],
        }
        await self.collection.insert_one(document, session=self.session)

        return data.no

    async def update(self, no: PokemonNumberStr, data: UpdatePokemonModel):
        if data.name is not None:
            result = await self.collection.update_one(
                {'no': no},
                {self.SET: {'name': data.name}},
                session=self.session,
            )
            if result.matched_count == 0:
                raise PokemonNotFound(no)

    async def delete(self, no: PokemonNumberStr):
        pokemon = await self.collection.find_one({'no': no}, session=self.session)
        result = await self.collection.delete_one(
            {'no': no},
            session=self.session,
        )
        if result.deleted_count == 0 or not pokemon:
            raise PokemonNotFound(no)

        await self.collection.update_many(
            {'previous_evolution_object_ids': pokemon['_id']},
            {'$pull': {'previous_evolution_object_ids': pokemon['_id']}},
            session=self.session,
        )
        await self.collection.update_many(
            {'next_evolution_object_ids': pokemon['_id']},
            {'$pull': {'next_evolution_object_ids': pokemon['_id']}},
            session=self.session,
        )

    async def are_existed(self, numbers: List[PokemonNumberStr]) -> bool:
        count = await self.collection.count_documents(
            {'no': {'$in': numbers}}, session=self.session
        )
        return count == len(numbers)

    async def replace_types(self, pokemon_no: PokemonNumberStr, type_names: List[str]):
        await self.collection.update_one(
            {'no': pokemon_no},
            {self.SET: {'types': type_names}},
            session=self.session,
        )

    async def replace_previous_evolutions(
        self, pokemon_no: PokemonNumberStr, previous_evolution_numbers: List[PokemonNumberStr]
    ):
        number_to_object_id_map = await self._get_filtered_pokemon_id_map(
            [pokemon_no] + previous_evolution_numbers
        )
        object_id = number_to_object_id_map.pop(pokemon_no)

        result = await self.collection.update_one(
            {'_id': object_id},
            {self.SET: {'previous_evolution_object_ids': list(number_to_object_id_map.values())}},
            session=self.session,
        )
        if result.matched_count == 0:
            raise PokemonNotFound(pokemon_no)

        await self.collection.update_many(
            {'_id': {'$in': list(number_to_object_id_map.values())}},
            {self.PUSH: {'next_evolution_object_ids': object_id}},
            session=self.session,
        )

    async def replace_next_evolutions(
        self, pokemon_no: PokemonNumberStr, next_evolution_numbers: List[PokemonNumberStr]
    ):
        number_to_object_id_map = await self._get_filtered_pokemon_id_map(
            [pokemon_no] + next_evolution_numbers
        )
        object_id = number_to_object_id_map.pop(pokemon_no)

        result = await self.collection.update_one(
            {'_id': object_id},
            {self.SET: {'next_evolution_object_ids': list(number_to_object_id_map.values())}},
            session=self.session,
        )
        if result.matched_count == 0:
            raise PokemonNotFound(pokemon_no)

        await self.collection.update_many(
            {'_id': {'$in': list(number_to_object_id_map.values())}},
            {self.PUSH: {'previous_evolution_object_ids': object_id}},
            session=self.session,
        )
