import re
from typing import List

from redis.asyncio import StrictRedis as AsyncRedis

from common.type import PokemonNumberStr, UUIDStr
from common.utils import build_uuid4_str
from models.exception import TrainerNotFound
from models.trainer import (
    CreateTrainerModel,
    TrainerModel,
    UpdateTrainerModel,
)

from ...abstraction import AbstractTrainerRepository
from .mapper import TrainerKeyValueMapper


class RedisTrainerRepository(AbstractTrainerRepository):
    re_pattern = re.compile(r'TRAINER:([a-fA-F0-9]{32}):INFO')

    def __init__(self, client: AsyncRedis):
        self.client: AsyncRedis = client

    def _build_info_key(self, id: UUIDStr) -> str:
        return f'TRAINER:{id}:INFO'

    def _build_team_key(self, id: UUIDStr) -> str:
        return f'TRAINER:{id}:TEAM'

    def _build_pokemon_info_key(self, no: PokemonNumberStr) -> str:
        return f'POKEMON:{no}:INFO'

    async def get(self, id: UUIDStr) -> TrainerModel:
        key = self._build_info_key(id)
        if not await self.client.exists(key):
            raise TrainerNotFound(id)

        async with self.client.pipeline() as pipe:
            pipe.hgetall(key)
            pipe.smembers(self._build_team_key(id))
            [info, team_numbers] = await pipe.execute()

            team = []
            for number in sorted(team_numbers):
                pipe.hgetall(self._build_pokemon_info_key(number))
            pokemon_infos = await pipe.execute()
            for pokemon_info in pokemon_infos:
                if pokemon_info:
                    team.append({'no': pokemon_info['no'], 'name': pokemon_info['name']})

            return TrainerKeyValueMapper.dict_to_entity({**info, 'team': team})

    async def list(self) -> List[TrainerModel]:
        trainers = []
        async with self.client.pipeline() as pipe:
            async for key in self.client.scan_iter(match='TRAINER:*:INFO'):
                match = self.re_pattern.match(key)
                if not match:
                    continue

                id = UUIDStr(match.group(1))
                pipe.hgetall(self._build_info_key(id))
                pipe.smembers(self._build_team_key(id))
                [info, team_numbers] = await pipe.execute()

                team = []
                for number in sorted(team_numbers):
                    pipe.hgetall(self._build_pokemon_info_key(number))
                pokemon_infos = await pipe.execute()
                for pokemon_info in pokemon_infos:
                    if pokemon_info:
                        team.append({'no': pokemon_info['no'], 'name': pokemon_info['name']})

                trainers.append(TrainerKeyValueMapper.dict_to_entity({**info, 'team': team}))

        return sorted(trainers, key=lambda t: t.id)

    async def create(self, data: CreateTrainerModel) -> UUIDStr:
        id = UUIDStr(build_uuid4_str())
        key = self._build_info_key(id)

        async with self.client.pipeline() as pipe:
            pipe.hset(key, 'id', id)
            pipe.hset(key, 'name', data.name)
            pipe.hset(key, 'region', data.region)
            pipe.hset(key, 'badge_count', str(data.badge_count))
            await pipe.execute()

        return id

    async def update(self, id: UUIDStr, data: UpdateTrainerModel):
        key = self._build_info_key(id)
        if not await self.client.exists(key):
            raise TrainerNotFound(id)

        async with self.client.pipeline() as pipe:
            if data.name is not None:
                pipe.hset(key, 'name', data.name)
            if data.region is not None:
                pipe.hset(key, 'region', data.region)
            if data.badge_count is not None:
                pipe.hset(key, 'badge_count', str(data.badge_count))
            await pipe.execute()

    async def delete(self, id: UUIDStr):
        info_key = self._build_info_key(id)
        if not await self.client.exists(info_key):
            raise TrainerNotFound(id)

        team_key = self._build_team_key(id)
        async with self.client.pipeline() as pipe:
            pipe.delete(info_key)
            pipe.delete(team_key)
            await pipe.execute()

    async def add_to_team(self, trainer_id: UUIDStr, pokemon_no: PokemonNumberStr):
        await self.client.sadd(self._build_team_key(trainer_id), pokemon_no)

    async def remove_from_team(self, trainer_id: UUIDStr, pokemon_no: PokemonNumberStr):
        await self.client.srem(self._build_team_key(trainer_id), pokemon_no)

    async def remove_pokemon_from_all_teams(self, pokemon_no: PokemonNumberStr):
        async for key in self.client.scan_iter(match='TRAINER:*:TEAM'):
            await self.client.srem(key, pokemon_no)
