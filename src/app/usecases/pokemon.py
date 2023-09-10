from app.di.dependency_injection import async_unit_of_work
from common.type import PokemonNumberStr
from models.exception import PokemonNotFound
from models.pokemon import CreatePokemonModel, PokemonModel, UpdatePokemonModel


async def create_pokemon(data: CreatePokemonModel) -> PokemonModel:
    async with async_unit_of_work() as auow:
        pokemon_no = await auow.pokemon_repo.create(data)

        types = [await auow.type_repo.get_or_create(type_) for type_ in data.type_names]
        await auow.pokemon_repo.put_types(pokemon_no, types)

        if data.before_evolution_numbers:
            if not await auow.pokemon_repo.are_duplicated(data.before_evolution_numbers):
                raise PokemonNotFound(data.before_evolution_numbers)
            await auow.pokemon_repo.put_before_evolutions(pokemon_no, data.before_evolution_numbers)
        if data.after_evolution_numbers:
            if not await auow.pokemon_repo.are_duplicated(data.after_evolution_numbers):
                raise PokemonNotFound(data.after_evolution_numbers)
            await auow.pokemon_repo.put_after_evolutions(pokemon_no, data.after_evolution_numbers)

        return await auow.pokemon_repo.get(pokemon_no)


async def get_pokemon(no: PokemonNumberStr) -> PokemonModel:
    async with async_unit_of_work() as auow:
        return await auow.pokemon_repo.get(no)


async def get_pokemons() -> list[PokemonModel]:
    async with async_unit_of_work() as auow:
        return await auow.pokemon_repo.list_()


async def update_pokemon(no: PokemonNumberStr, data: UpdatePokemonModel):
    async with async_unit_of_work() as auow:
        await auow.pokemon_repo.update(no, data)

        if data.type_names is not None:
            types = [await auow.type_repo.get_or_create(type_) for type_ in data.type_names]
            await auow.pokemon_repo.put_types(no, types)

        if data.before_evolution_numbers is not None:
            if not await auow.pokemon_repo.are_duplicated(data.before_evolution_numbers):
                raise PokemonNotFound(data.before_evolution_numbers)
            await auow.pokemon_repo.put_before_evolutions(no, data.before_evolution_numbers)
        if data.after_evolution_numbers is not None:
            if not await auow.pokemon_repo.are_duplicated(data.after_evolution_numbers):
                raise PokemonNotFound(data.after_evolution_numbers)
            await auow.pokemon_repo.put_after_evolutions(no, data.after_evolution_numbers)

        return await auow.pokemon_repo.get(no)


async def delete_pokemon(no: PokemonNumberStr):
    async with async_unit_of_work() as auow:
        await auow.pokemon_repo.delete(no)
