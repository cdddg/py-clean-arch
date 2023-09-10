from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import delete, func, insert, select, update

from common.type import PokemonNumberStr, UUIDStr
from models.exception import PokemonNotFound
from models.pokemon import (
    CreatePokemonModel,
    GetPokemonParamsModel,
    GetTypeParamsModel,
    PokemonEvolutionModel,
    PokemonModel,
    TypeModel,
    UpdatePokemonModel,
)

from .mapper import PokemonOrmMapper, TypeOrmMapper
from .orm import Pokemon, PokemonEvolution, PokemonType, Type

func: Callable


class PokemonRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, no: PokemonNumberStr) -> PokemonModel:
        stmt = (
            select(Pokemon)
            .where(Pokemon.no == no)
            .options(
                selectinload(Pokemon.types),
                selectinload(Pokemon.before_evolutions).joinedload(PokemonEvolution.before_pokemon),
                selectinload(Pokemon.after_evolutions).joinedload(PokemonEvolution.after_pokemon),
            )
        )
        pokemon = (await self.session.execute(stmt)).scalars().one_or_none()
        if not pokemon:
            raise PokemonNotFound(no)

        return PokemonOrmMapper.orm_to_entity(pokemon)

    async def list_(self, params: Optional[GetPokemonParamsModel] = None) -> list[PokemonModel]:
        stmt = select(Pokemon).options(
            selectinload(Pokemon.types),
            selectinload(Pokemon.before_evolutions).joinedload(PokemonEvolution.before_pokemon),
            selectinload(Pokemon.after_evolutions).joinedload(PokemonEvolution.after_pokemon),
        )
        if params:
            stmt = stmt.offset(params.offset).limit(params.limit)
        pokemons = (await self.session.execute(stmt)).scalars().all()

        return list(map(PokemonOrmMapper.orm_to_entity, pokemons))

    async def create(self, data: CreatePokemonModel) -> PokemonNumberStr:
        stmt = insert(Pokemon).values(no=data.no, name=data.name)
        await self.session.execute(stmt)

        return data.no

    async def update(self, no: PokemonNumberStr, data: UpdatePokemonModel):
        if data.name:
            stmt = update(Pokemon).where(Pokemon.no == no).values(name=data.name)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                raise PokemonNotFound(no)

    async def delete(self, no: PokemonNumberStr):
        stmt = delete(Pokemon).where(Pokemon.no == no)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise PokemonNotFound(no)

    async def are_duplicated(self, numbers: list[PokemonNumberStr]) -> bool:
        stmt = select(func.count(Pokemon.no)).where(Pokemon.no.in_(numbers))
        count = (await self.session.execute(stmt)).scalars().first()

        return count == len(numbers)

    async def put_types(self, pokemon_no: PokemonNumberStr, types: list[TypeModel]):
        stmt = delete(PokemonType).where(PokemonType.pokemon_no == pokemon_no)
        await self.session.execute(stmt)

        stmt = insert(PokemonType)
        for type_ in types:
            stmt = stmt.values(pokemon_no=pokemon_no, type_id=type_.id)
            await self.session.execute(stmt)

    async def put_before_evolutions(
        self, pokemon_no: PokemonNumberStr, before_evolution_numbers: list[PokemonNumberStr]
    ):
        stmt = delete(PokemonEvolution).where(PokemonEvolution.after_no == pokemon_no)
        await self.session.execute(stmt)

        stmt = insert(PokemonEvolution)
        for no in before_evolution_numbers:
            stmt = stmt.values(before_no=no, after_no=pokemon_no)
            await self.session.execute(stmt)

    async def put_after_evolutions(
        self, pokemon_no: PokemonNumberStr, after_evolution_numbers: list[PokemonNumberStr]
    ):
        stmt = delete(PokemonEvolution).where(PokemonEvolution.before_no == pokemon_no)
        await self.session.execute(stmt)

        stmt = insert(PokemonEvolution)
        for no in after_evolution_numbers:
            stmt = stmt.values(before_no=pokemon_no, after_no=no)
            await self.session.execute(stmt)


class TypeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, type_id: UUIDStr) -> TypeModel:
        raise NotImplementedError

    async def list_(self, params: Optional[GetTypeParamsModel] = None) -> list[TypeModel]:
        stmt = select(Type)
        types = (await self.session.execute(stmt)).scalars().all()

        return list(map(TypeOrmMapper.orm_to_entity, types))

    async def get_or_create(self, name: str) -> TypeModel:
        stmt = select(Type).filter(Type.name == name)
        type_ = (await self.session.execute(stmt)).scalars().one_or_none()
        if not type_:
            type_ = Type(name=name)
            self.session.add(type_)
            await self.session.flush()

        return TypeOrmMapper.orm_to_entity(type_)


class EvolutionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _convert_evolution_to_model(pokemon: Pokemon) -> PokemonEvolutionModel:
        raise NotImplementedError

    @classmethod
    async def list_(cls) -> list[PokemonEvolutionModel]:
        raise NotImplementedError
