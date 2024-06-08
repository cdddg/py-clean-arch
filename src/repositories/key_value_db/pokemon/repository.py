import re
from typing import List, Optional

from redis.asyncio import StrictRedis as AsyncRedis

from common.type import PokemonNumberStr
from models.exception import PokemonAlreadyExists, PokemonNotFound, PokemonUnknownError
from models.pokemon import (
    CreatePokemonModel,
    GetPokemonParamsModel,
    PokemonModel,
    UpdatePokemonModel,
)

from ...abstraction import AbstractPokemonRepository
from .mapper import PokemonKeyValueMapper


class RedisPokemonRepository(AbstractPokemonRepository):
    re_pattern = re.compile(r'POKEMON:(\d+):INFO')

    def __init__(self, client: AsyncRedis):
        self.client: AsyncRedis = client

    def _build_info_key(self, no: PokemonNumberStr) -> str:
        return f'POKEMON:{no}:INFO'

    def _build_type_key(self, no: PokemonNumberStr) -> str:
        return f'POKEMON:{no}:TYPE'

    def _build_previous_evolution_key(self, no: PokemonNumberStr) -> str:
        return f'POKEMON:{no}:PREVIOUS_EVOLUTION'

    def _build_next_evolution_key(self, no: PokemonNumberStr) -> str:
        return f'POKEMON:{no}:NEXT_EVOLUTION'

    async def get(self, no: PokemonNumberStr):
        key = self._build_info_key(no)
        if not await self.client.exists(key):
            raise PokemonNotFound(no)

        async with self.client.pipeline() as pipe:
            pipe.hgetall(key)
            pipe.smembers(self._build_type_key(no))
            pipe.smembers(self._build_previous_evolution_key(no))
            pipe.smembers(self._build_next_evolution_key(no))
            [info, types, prev_evo_numbers, next_evo_numbers] = await pipe.execute()

            for number in prev_evo_numbers:
                pipe.hgetall(self._build_info_key(number))
            prev_evos = await pipe.execute()
            for number in next_evo_numbers:
                pipe.hgetall(self._build_info_key(number))
            next_evos = await pipe.execute()

            return PokemonKeyValueMapper.dict_to_entity(
                {
                    **info,
                    'types': sorted(types),
                    'previous_evolutions': sorted(prev_evos, key=lambda item: item['no']),
                    'next_evolutions': sorted(next_evos, key=lambda item: item['no']),
                },
            )

    async def list(self, params: Optional[GetPokemonParamsModel] = None) -> List[PokemonModel]:
        pokemon_map = {}
        async with self.client.pipeline() as pipe:
            async for key in self.client.scan_iter(match='POKEMON:*:INFO'):
                match = self.re_pattern.match(key)
                if not match:
                    raise PokemonUnknownError(key)

                no = PokemonNumberStr(match.group(1))
                pipe.hgetall(self._build_info_key(no))
                pipe.smembers(self._build_type_key(no))
                pipe.smembers(self._build_previous_evolution_key(no))
                pipe.smembers(self._build_next_evolution_key(no))
                [info, types, prev_evo_numbers, next_evo_numbers] = await pipe.execute()

                for number in list(prev_evo_numbers) + list(next_evo_numbers):
                    if number == no:
                        continue
                    if number not in pokemon_map:
                        pipe.hgetall(self._build_info_key(number))
                for evo_info in await pipe.execute():
                    pokemon_map[evo_info['no']] = evo_info

                pokemon_map[no] = info
                pokemon_map[no]['types'] = sorted(types)
                pokemon_map[no]['previous_evolutions'] = [
                    {'no': pokemon_map[number]['no'], 'name': pokemon_map[number]['name']}
                    for number in sorted(prev_evo_numbers)
                ]
                pokemon_map[no]['next_evolutions'] = [
                    {'no': pokemon_map[number]['no'], 'name': pokemon_map[number]['name']}
                    for number in sorted(next_evo_numbers)
                ]

        return list(
            map(
                PokemonKeyValueMapper.dict_to_entity,
                sorted(pokemon_map.values(), key=lambda pokemon: pokemon['no']),
            )
        )

    async def create(self, data: CreatePokemonModel) -> PokemonNumberStr:
        key = self._build_info_key(data.no)
        if await self.client.exists(key):
            raise PokemonAlreadyExists(data.no)

        async with self.client.pipeline() as pipe:
            pipe.hset(key, 'no', data.no)
            pipe.hset(key, 'name', data.name)
            pipe.hset(key, 'hp', '')
            pipe.hset(key, 'attack', '')
            pipe.hset(key, 'defense', '')
            pipe.hset(key, 'sp_atk', '')
            pipe.hset(key, 'sp_def', '')
            pipe.hset(key, 'speed', '')
            await pipe.execute()

        return data.no

    async def update(self, no: PokemonNumberStr, data: UpdatePokemonModel):
        if data.name is not None:
            key = self._build_info_key(no)
            if not await self.client.exists(key):
                raise PokemonNotFound(no)

            await self.client.hset(key, 'name', data.name)

    async def delete(self, no: PokemonNumberStr):
        # pylint: disable=too-many-locals

        info_key = self._build_info_key(no)
        type_key = self._build_type_key(no)
        prev_evo_key = self._build_previous_evolution_key(no)
        next_evo_key = self._build_next_evolution_key(no)

        is_existed = await self.client.exists(info_key)
        if not is_existed:
            raise PokemonNotFound(no)

        async with self.client.pipeline() as pipe:
            pipe.hgetall(info_key)
            pipe.smembers(type_key)
            pipe.smembers(prev_evo_key)
            pipe.smembers(next_evo_key)
            [_, _, ori_prev_evo_numbers, ori_next_evo_numbers] = await pipe.execute()

            pipe.delete(info_key)
            pipe.delete(type_key)
            pipe.delete(prev_evo_key)
            pipe.delete(next_evo_key)
            await pipe.execute()

            for number in ori_prev_evo_numbers:
                key = self._build_next_evolution_key(number)
                pipe.srem(key, no)
            for number in ori_next_evo_numbers:
                key = self._build_previous_evolution_key(number)
                pipe.srem(key, no)

            await pipe.execute()

    async def are_existed(self, numbers: List[PokemonNumberStr]) -> bool:
        if not numbers:
            return True

        async with self.client.pipeline() as pipe:
            for number in numbers:
                pipe.exists(self._build_info_key(number))
            return any(await pipe.execute())

    async def replace_types(self, pokemon_no: PokemonNumberStr, type_names: List[str]):
        key = self._build_type_key(pokemon_no)
        await self.client.delete(key)
        await self.client.sadd(key, *type_names)

    async def replace_previous_evolutions(
        self, pokemon_no: PokemonNumberStr, previous_evolution_numbers: List[PokemonNumberStr]
    ):
        async with self.client.pipeline() as pipe:
            ori_prev_evo_numbers = await self.client.smembers(
                self._build_previous_evolution_key(pokemon_no)
            )
            for number in ori_prev_evo_numbers:
                key = self._build_next_evolution_key(number)
                pipe.srem(key, pokemon_no)

            key = self._build_previous_evolution_key(pokemon_no)
            pipe.delete(key)

            for number in previous_evolution_numbers:
                key = self._build_previous_evolution_key(pokemon_no)
                pipe.sadd(key, number)
                key = self._build_next_evolution_key(number)
                pipe.sadd(key, pokemon_no)

            await pipe.execute()

    async def replace_next_evolutions(
        self, pokemon_no: PokemonNumberStr, next_evolution_numbers: List[PokemonNumberStr]
    ):
        async with self.client.pipeline() as pipe:
            ori_next_evo_numbers = await self.client.smembers(
                self._build_next_evolution_key(pokemon_no)
            )
            for number in ori_next_evo_numbers:
                key = self._build_previous_evolution_key(number)
                pipe.srem(key, pokemon_no)

            key = self._build_next_evolution_key(pokemon_no)
            pipe.delete(key)

            for number in next_evolution_numbers:
                key = self._build_next_evolution_key(pokemon_no)
                pipe.sadd(key, number)
                key = self._build_previous_evolution_key(number)
                pipe.sadd(key, pokemon_no)

            await pipe.execute()
