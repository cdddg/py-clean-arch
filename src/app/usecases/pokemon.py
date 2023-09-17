from app.di.dependency_injection import async_unit_of_work
from common.type import PokemonNumberStr
from models.exception import PokemonNotFound
from models.pokemon import CreatePokemonModel, PokemonModel, UpdatePokemonModel


async def create_pokemon(data: CreatePokemonModel) -> PokemonModel:
    async with async_unit_of_work() as auow:
        no = await auow.pokemon_repo.create(data)
        await auow.pokemon_repo.replace_types(no, data.type_names)

        if data.previous_evolution_numbers:
            if not await auow.pokemon_repo.are_existed(data.previous_evolution_numbers):
                raise PokemonNotFound(data.previous_evolution_numbers)
            await auow.pokemon_repo.replace_previous_evolutions(no, data.previous_evolution_numbers)
        if data.next_evolution_numbers:
            if not await auow.pokemon_repo.are_existed(data.next_evolution_numbers):
                raise PokemonNotFound(data.next_evolution_numbers)
            await auow.pokemon_repo.replace_next_evolutions(no, data.next_evolution_numbers)

        # raise RuntimeWarning('Not Implemented')
        return await auow.pokemon_repo.get(no)


async def get_pokemon(no: PokemonNumberStr) -> PokemonModel:
    async with async_unit_of_work() as auow:
        return await auow.pokemon_repo.get(no)


async def get_pokemons() -> list[PokemonModel]:
    async with async_unit_of_work() as auow:
        return await auow.pokemon_repo.list()


async def update_pokemon(no: PokemonNumberStr, data: UpdatePokemonModel):
    async with async_unit_of_work() as auow:
        await auow.pokemon_repo.update(no, data)

        if data.type_names is not None:
            await auow.pokemon_repo.replace_types(no, data.type_names)

        if data.previous_evolution_numbers is not None:
            if not await auow.pokemon_repo.are_existed(data.previous_evolution_numbers):
                raise PokemonNotFound(data.previous_evolution_numbers)
            await auow.pokemon_repo.replace_previous_evolutions(no, data.previous_evolution_numbers)
        if data.next_evolution_numbers is not None:
            if not await auow.pokemon_repo.are_existed(data.next_evolution_numbers):
                raise PokemonNotFound(data.next_evolution_numbers)
            await auow.pokemon_repo.replace_next_evolutions(no, data.next_evolution_numbers)

        return await auow.pokemon_repo.get(no)


async def delete_pokemon(no: PokemonNumberStr):
    async with async_unit_of_work() as auow:
        await auow.pokemon_repo.delete(no)
