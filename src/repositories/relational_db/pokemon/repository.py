from typing import Callable, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import delete, func, insert, select, update

from common.type import PokemonNumberStr
from models.exception import PokemonAlreadyExists, PokemonNotFound
from models.pokemon import (
    CreatePokemonModel,
    GetPokemonParamsModel,
    PokemonModel,
    UpdatePokemonModel,
)

from ...abstraction import AbstractPokemonRepository
from .mapper import PokemonOrmMapper
from .orm import Pokemon, PokemonEvolution, PokemonType, Type

func: Callable


class RelationalDBPokemonRepository(AbstractPokemonRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, no: PokemonNumberStr) -> PokemonModel:
        stmt = (
            select(Pokemon)
            .where(Pokemon.no == no)
            .options(
                selectinload(Pokemon.types),
                selectinload(Pokemon.previous_evolutions).joinedload(
                    PokemonEvolution.previous_pokemon
                ),
                selectinload(Pokemon.next_evolutions).joinedload(PokemonEvolution.next_pokemon),
            )
        )
        pokemon = (await self.session.execute(stmt)).scalars().one_or_none()
        if not pokemon:
            raise PokemonNotFound(no)

        return PokemonOrmMapper.orm_to_entity(pokemon)

    async def list(self, params: Optional[GetPokemonParamsModel] = None) -> List[PokemonModel]:
        stmt = select(Pokemon).options(
            selectinload(Pokemon.types),
            selectinload(Pokemon.previous_evolutions).joinedload(PokemonEvolution.previous_pokemon),
            selectinload(Pokemon.next_evolutions).joinedload(PokemonEvolution.next_pokemon),
        )
        if params:
            stmt = stmt.offset((params.page - 1) * params.size).limit(params.size)
        pokemons = (await self.session.execute(stmt)).scalars().all()

        return list(map(PokemonOrmMapper.orm_to_entity, pokemons))

    async def create(self, data: CreatePokemonModel) -> PokemonNumberStr:
        stmt = select(func.count(Pokemon.no)).where(Pokemon.no == data.no)
        count = (await self.session.execute(stmt)).scalars().first()
        if count and count > 0:
            raise PokemonAlreadyExists(data.no)

        stmt = insert(Pokemon).values(no=data.no, name=data.name)
        await self.session.execute(stmt)

        return data.no

    async def update(self, no: PokemonNumberStr, data: UpdatePokemonModel):
        if data.name is not None:
            stmt = update(Pokemon).where(Pokemon.no == no).values(name=data.name)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                raise PokemonNotFound(no)

    async def delete(self, no: PokemonNumberStr):
        stmt = delete(Pokemon).where(Pokemon.no == no)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise PokemonNotFound(no)

    async def are_existed(self, numbers: List[PokemonNumberStr]) -> bool:
        stmt = select(func.count(Pokemon.no)).where(Pokemon.no.in_(numbers))
        count = (await self.session.execute(stmt)).scalars().first()

        return count == len(numbers)

    async def replace_types(self, pokemon_no: PokemonNumberStr, type_names: List[str]):
        await self.session.execute(delete(PokemonType).where(PokemonType.pokemon_no == pokemon_no))

        stmt = select(Type).where(Type.name.in_(type_names))
        existing_types = (await self.session.execute(stmt)).scalars().all()
        existing_type_name_to_id_map = {type_.name: type_.id for type_ in existing_types}

        to_be_created_names = [
            name for name in type_names if name not in existing_type_name_to_id_map
        ]
        if new_types := [Type(name=name) for name in to_be_created_names]:
            self.session.add_all(new_types)
            await self.session.flush()

        stmt = insert(PokemonType).values(
            [
                {'pokemon_no': pokemon_no, 'type_id': type_id}
                for type_id in list(existing_type_name_to_id_map.values())
                + [type_.id for type_ in new_types]
            ]
        )
        await self.session.execute(stmt)

    async def replace_previous_evolutions(
        self, pokemon_no: PokemonNumberStr, previous_evolution_numbers: List[PokemonNumberStr]
    ):
        stmt = delete(PokemonEvolution).where(PokemonEvolution.next_no == pokemon_no)
        await self.session.execute(stmt)

        if previous_evolution_numbers:
            stmt = insert(PokemonEvolution).values(
                [{'previous_no': no, 'next_no': pokemon_no} for no in previous_evolution_numbers]
            )
            await self.session.execute(stmt)

    async def replace_next_evolutions(
        self, pokemon_no: PokemonNumberStr, next_evolution_numbers: List[PokemonNumberStr]
    ):
        stmt = delete(PokemonEvolution).where(PokemonEvolution.previous_no == pokemon_no)
        await self.session.execute(stmt)

        if next_evolution_numbers:
            stmt = insert(PokemonEvolution).values(
                [{'previous_no': pokemon_no, 'next_no': no} for no in next_evolution_numbers]
            )
            await self.session.execute(stmt)
