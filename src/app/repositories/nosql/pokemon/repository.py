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
    def __init__(
        self,
        collection: AsyncIOMotorCollection,
        session: Optional[AsyncIOMotorClientSession] = None,
    ):
        self.collection = collection
        self.session = session

    def _build_evolution_pipeline(self) -> List:
        return [
            {
                '$lookup': {
                    'from': self.collection.name,
                    'localField': 'previous_evolutions',
                    'foreignField': '_id',
                    'as': 'previous_evolutions_detail',
                }
            },
            {
                '$unwind': {
                    'path': '$previous_evolutions_detail',
                    'preserveNullAndEmptyArrays': True,
                }
            },
            {'$sort': {'previous_evolutions_detail.no': 1}},
            {
                '$group': {
                    '_id': '$_id',
                    'no': {'$first': '$no'},
                    'name': {'$first': '$name'},
                    'types': {'$first': '$types'},
                    'previous_evolutions': {'$first': '$previous_evolutions'},
                    'next_evolutions': {'$first': '$next_evolutions'},
                    'previous_evolutions_detail': {'$push': '$previous_evolutions_detail'},
                }
            },
            {
                '$lookup': {
                    'from': self.collection.name,
                    'localField': 'next_evolutions',
                    'foreignField': '_id',
                    'as': 'next_evolutions_detail',
                }
            },
            {'$unwind': {'path': '$next_evolutions_detail', 'preserveNullAndEmptyArrays': True}},
            {'$sort': {'next_evolutions_detail.no': 1}},
            {
                '$group': {
                    '_id': '$_id',
                    'no': {'$first': '$no'},
                    'name': {'$first': '$name'},
                    'types': {'$first': '$types'},
                    'previous_evolutions': {'$first': '$previous_evolutions'},
                    'previous_evolutions_detail': {'$first': '$previous_evolutions_detail'},
                    'next_evolutions': {'$first': '$next_evolutions'},
                    'next_evolutions_detail': {'$push': '$next_evolutions_detail'},
                }
            },
        ]

    async def _get_pokemon_no_to_object_id_map(
        self, numbers: List[PokemonNumberStr]
    ) -> dict[PokemonNumberStr, ObjectId]:
        cursor = self.collection.find({'no': {'$in': numbers}}, session=self.session)

        return {
            document['no']: document['_id']
            for document in await cursor.to_list(None)  # pyright: ignore[reportGeneralTypeIssues]
        }

    async def get(self, no: PokemonNumberStr):
        pipeline = self._build_evolution_pipeline()
        pipeline.append({'$match': {'no': no}})
        document = await self.collection.aggregate(pipeline, session=self.session).next()
        if not document:
            raise PokemonNotFound(no)

        return PokemonDictMapper.dict_to_entity(document)

    async def list(self, params: Optional[GetPokemonParamsModel] = None) -> List[PokemonModel]:
        pipeline = self._build_evolution_pipeline()
        pipeline.append({'$sort': {'no': 1}})
        # if params:
        #     pipeline.append({'$skip': params.offset})
        #     pipeline.append({'$limit': params.limit})
        cursor = self.collection.aggregate(pipeline, session=self.session)
        documents = await cursor.to_list(None)  # pyright: ignore[reportGeneralTypeIssues]

        return list(map(PokemonDictMapper.dict_to_entity, documents))

    async def create(self, data: CreatePokemonModel) -> PokemonNumberStr:
        count = await self.collection.count_documents({'no': data.no})
        if count > 0:
            raise PokemonAlreadyExists(data.no)

        document = {
            'no': data.no,
            'name': data.name,
            'types': [],
            'previous_evolutions': [],
            'next_evolutions': [],
        }
        await self.collection.insert_one(document, session=self.session)

        return data.no

    async def update(self, no: PokemonNumberStr, data: UpdatePokemonModel):
        res = await self.collection.update_one(
            {'no': no},
            {'$set': {'name': data.name}},
            session=self.session,
        )
        if res.matched_count == 0:
            raise PokemonNotFound(no)

    async def delete(self, no: PokemonNumberStr):
        res = await self.collection.delete_one({'no': no}, session=self.session)
        if res.deleted_count == 0:
            raise PokemonNotFound(no)

    async def are_existed(self, numbers: List[PokemonNumberStr]) -> bool:
        count = await self.collection.count_documents(
            {'no': {'$in': numbers}}, session=self.session
        )
        return count == len(numbers)

    async def replace_types(self, pokemon_no: PokemonNumberStr, type_names: List[str]):
        await self.collection.update_one(
            {'no': pokemon_no}, {'$set': {'types': type_names}}, session=self.session
        )

    async def replace_previous_evolutions(
        self, pokemon_no: PokemonNumberStr, previous_evolution_numbers: List[PokemonNumberStr]
    ):
        pokemon_no_to_object_id_map = await self._get_pokemon_no_to_object_id_map(
            [pokemon_no] + previous_evolution_numbers
        )
        object_id = pokemon_no_to_object_id_map.pop(pokemon_no)

        res = await self.collection.update_one(
            {'_id': object_id},
            {'$set': {'previous_evolutions': list(pokemon_no_to_object_id_map.values())}},
            session=self.session,
        )
        if res.matched_count == 0:
            raise PokemonNotFound(pokemon_no)

        await self.collection.update_many(
            {'_id': {'$in': list(pokemon_no_to_object_id_map.values())}},
            {'$push': {'next_evolutions': object_id}},
            session=self.session,
        )

    async def replace_next_evolutions(
        self, pokemon_no: PokemonNumberStr, next_evolution_numbers: List[PokemonNumberStr]
    ):
        pokemon_no_to_object_id_map = await self._get_pokemon_no_to_object_id_map(
            [pokemon_no] + next_evolution_numbers
        )
        object_id = pokemon_no_to_object_id_map.pop(pokemon_no)

        res = await self.collection.update_one(
            {'_id': object_id},
            {'$set': {'next_evolutions': list(pokemon_no_to_object_id_map.values())}},
            session=self.session,
        )
        if res.matched_count == 0:
            raise PokemonNotFound(pokemon_no)

        await self.collection.update_many(
            {'_id': {'$in': list(pokemon_no_to_object_id_map.values())}},
            {'$push': {'previous_evolutions': object_id}},
            session=self.session,
        )
