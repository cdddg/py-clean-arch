from core.exception import PokemonNotFound
from models.pokemon import CreatePokemonModel, PokemonModel, UpdatePokemonModel
from settings.dependency_injection import async_unit_of_work


async def create_pokemon(body: CreatePokemonModel) -> PokemonModel:
    async with async_unit_of_work() as auow:
        pokemon_no = await auow.pokemon_repo.create(body)

        types = [await auow.type_repo.get_or_create(type_) for type_ in body.type_names]
        await auow.pokemon_repo.put_types(pokemon_no, types)

        if body.before_evolution_numbers:
            if not await auow.pokemon_repo.are_duplicated(body.before_evolution_numbers):
                raise PokemonNotFound(body.before_evolution_numbers)
            await auow.pokemon_repo.put_before_evolutions(pokemon_no, body.before_evolution_numbers)
        if body.after_evolution_numbers:
            if not await auow.pokemon_repo.are_duplicated(body.after_evolution_numbers):
                raise PokemonNotFound(body.after_evolution_numbers)
            await auow.pokemon_repo.put_after_evolutions(pokemon_no, body.after_evolution_numbers)

        return await auow.pokemon_repo.get(pokemon_no)


async def get_pokemon(no: str) -> PokemonModel:
    async with async_unit_of_work() as auow:
        return await auow.pokemon_repo.get(no)


async def get_pokemons() -> list[PokemonModel]:
    async with async_unit_of_work() as auow:
        return await auow.pokemon_repo.list_()


async def update_pokemon(no: str, body: UpdatePokemonModel):
    async with async_unit_of_work() as auow:
        await auow.pokemon_repo.update(no, body)

        if body.type_names is not None:
            types = [await auow.type_repo.get_or_create(type_) for type_ in body.type_names]
            await auow.pokemon_repo.put_types(no, types)

        if body.before_evolution_numbers is not None:
            if not await auow.pokemon_repo.are_duplicated(body.before_evolution_numbers):
                raise PokemonNotFound(body.before_evolution_numbers)
            await auow.pokemon_repo.put_before_evolutions(no, body.before_evolution_numbers)
        if body.after_evolution_numbers is not None:
            if not await auow.pokemon_repo.are_duplicated(body.after_evolution_numbers):
                raise PokemonNotFound(body.after_evolution_numbers)
            await auow.pokemon_repo.put_after_evolutions(no, body.after_evolution_numbers)

        return await auow.pokemon_repo.get(no)


async def delete_pokemon(no: str):
    async with async_unit_of_work() as auow:
        await auow.pokemon_repo.delete(no)
