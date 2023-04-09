from typing import Optional
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlalchemy.sql import delete, func, insert, select, update

from core.exception import PokemonNotFound
from models.pokemon import (
    CreatePokemonModel,
    GetPokemonParamsModel,
    GetTypeParamsModel,
    PokemonEvolutionModel,
    PokemonModel,
    TypeModel,
    UpdatePokemonModel,
)
from settings.db import AsyncSession

from .orm import Pokemon, PokemonEvolution, PokemonType, Type


class PokemonRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _convert_pokemon_to_model(pokemon: Pokemon) -> PokemonModel:
        return PokemonModel(
            no=pokemon.no,
            name=pokemon.name,
            types=[TypeModel(id=type_.id, name=type_.name) for type_ in pokemon.types],
            before_evolutions=[
                PokemonEvolutionModel(
                    no=evo.before_pokemon.no,
                    name=evo.before_pokemon.name,
                )
                for evo in pokemon.before_evolutions
            ],
            after_evolutions=[
                PokemonEvolutionModel(
                    no=evo.after_pokemon.no,
                    name=evo.after_pokemon.name,
                )
                for evo in pokemon.after_evolutions
            ],
        )

    async def get(self, no: str) -> PokemonModel:
        stmt = (
            select(Pokemon)
            .where(Pokemon.no == no)
            .options(  # type: ignore
                selectinload(Pokemon.types),
                selectinload(Pokemon.before_evolutions).joinedload(PokemonEvolution.before_pokemon),
                selectinload(Pokemon.after_evolutions).joinedload(PokemonEvolution.after_pokemon),
            )
        )
        pokemon = (await self.session.execute(stmt)).scalars().one_or_none()
        if not pokemon:
            raise PokemonNotFound(no)

        return self._convert_pokemon_to_model(pokemon)

    async def list_(self, params: Optional[GetPokemonParamsModel] = None) -> list[PokemonModel]:
        stmt = select(Pokemon).options(  # type: ignore
            selectinload(Pokemon.types),
            selectinload(Pokemon.before_evolutions).joinedload(PokemonEvolution.before_pokemon),
            selectinload(Pokemon.after_evolutions).joinedload(PokemonEvolution.after_pokemon),
        )
        if params:
            stmt = stmt.offset(params.offset).limit(params.limit)
        pokemons = (await self.session.execute(stmt)).scalars().all()

        return list(map(self._convert_pokemon_to_model, pokemons))

    async def create(self, body: CreatePokemonModel) -> str:
        stmt = insert(Pokemon).values(no=body.no, name=body.name)
        await self.session.execute(stmt)

        return body.no

    async def update(self, no: str, body: UpdatePokemonModel):
        if body.name:
            stmt = update(Pokemon).where(Pokemon.no == no).values(name=body.name)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                raise PokemonNotFound(no)

    async def delete(self, no: str):
        stmt = delete(Pokemon).where(Pokemon.no == no)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise PokemonNotFound(no)

    async def are_duplicated(self, numbers: list[str]) -> bool:
        stmt = select(func.count(Pokemon.no)).where(Pokemon.no.in_(numbers))
        count = (await self.session.execute(stmt)).scalars().first()

        return count == len(numbers)

    async def put_types(self, pokemon_no: str, types: list[TypeModel]):  # type: ignore
        stmt = delete(PokemonType).where(PokemonType.pokemon_no == pokemon_no)
        await self.session.execute(stmt)

        stmt = insert(PokemonType)
        for type_ in types:
            stmt = stmt.values(pokemon_no=pokemon_no, type_id=type_.id)
            await self.session.execute(stmt)

    async def put_before_evolutions(self, pokemon_no: str, before_evolution_numbers: list[str]):
        stmt = delete(PokemonEvolution).where(PokemonEvolution.after_no == pokemon_no)
        await self.session.execute(stmt)

        stmt = insert(PokemonEvolution)
        for no in before_evolution_numbers:
            stmt = stmt.values(before_no=no, after_no=pokemon_no)
            await self.session.execute(stmt)

    async def put_after_evolutions(self, pokemon_no: str, after_evolution_numbers: list[str]):
        stmt = delete(PokemonEvolution).where(PokemonEvolution.before_no == pokemon_no)
        await self.session.execute(stmt)

        stmt = insert(PokemonEvolution)
        for no in after_evolution_numbers:
            stmt = stmt.values(before_no=pokemon_no, after_no=no)
            await self.session.execute(stmt)


class TypeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _convert_type_to_model(type_: Type) -> TypeModel:
        return TypeModel(id=type_.id, name=type_.name)  # type: ignore

    async def get(self, type_id: UUID) -> TypeModel:
        raise NotImplementedError

    async def list_(self, params: Optional[GetTypeParamsModel] = None) -> list[TypeModel]:
        stmt = select(Type)
        types = (await self.session.execute(stmt)).scalars().all()

        return list(map(self._convert_type_to_model, types))

    async def get_or_create(self, name: str) -> TypeModel:
        stmt = select(Type).filter(Type.name == name)  # type: ignore
        type_ = (await self.session.execute(stmt)).scalars().one_or_none()
        if not type_:
            type_ = Type(name=name)
            self.session.add(type_)
            await self.session.flush()

        return self._convert_type_to_model(type_)


class EvolutionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _convert_evolution_to_model(pokemon: Pokemon) -> PokemonEvolutionModel:
        raise NotImplementedError

    @classmethod
    async def list_(cls) -> list[PokemonEvolutionModel]:
        raise NotImplementedError


#     def update_relationships_id(self, rows_id: list[str], relationship_id: str):
#         return (
#             self._session.query(self.MODEL_CLS)
#             .filter(self.MODEL_CLS.relationship_id.in_(rows_id))
#             .update(dict(relationship_id=relationship_id))
#         )

#     def delete(self, pokemon_no: str):
#         return (
#             self._session.query(self.MODEL_CLS)
#             .filter_by(no=pokemon_no)
#             .delete()
#         )


# class EvolutionRepository(BaseRepository):
#     MODEL_CLS = Evolution

#     def get_or_create(self, before_id: str, after_id: str):
#         pokemon = (
#             self._session.query(self.MODEL_CLS)
#             .filter_by(before_id=before_id, after_id=after_id)
#             .one_or_none()
#         )
#         if not pokemon:
#             pokemon = self.add(
#                 self.MODEL_CLS(
#                     before_id=before_id,
#                     after_id=after_id,
#                 )
#             )

#         return pokemon

#     def delete_before_pokemon(self, before_id: str):
#         return (
#             self._session.query(self.MODEL_CLS)
#             .filter_by(before_id=before_id)
#             .delete()
#         )

#     def delete_after_pokemon(self, after_id: str):
#         return (
#             self._session.query(self.MODEL_CLS)
#             .filter_by(after_id=after_id)
#             .delete()
#         )


# pokemon_repo = PokemonRepository()
# type_repo = TypeRepository()
# pokemon_type_repo = PokemonTypeRepository()
# evolution_repo = EvolutionRepository()
