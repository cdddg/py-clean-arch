from fastapi import status
from fastapi_utils.inferring_router import InferringRouter

from pkg.usecases import pokemon as pokemon_ucase

from .schema import CreatePokemonRequest, PokemonResponse, UpdatePokemonRequest

router = InferringRouter(tags=['Pokemon'])


@router.post('/pokemons', status_code=status.HTTP_201_CREATED)
async def create_pokemon(body: CreatePokemonRequest) -> PokemonResponse:
    created_pokemon = await pokemon_ucase.create_pokemon(body.to_model())
    return PokemonResponse.from_model(created_pokemon)


@router.get('/pokemons/{no}')
async def get_pokemon(no: str) -> PokemonResponse:
    pokemon = await pokemon_ucase.get_pokemon(no)

    return PokemonResponse.from_model(pokemon)


@router.get('/pokemons')
async def get_pokemons() -> list[PokemonResponse]:
    pokemons = await pokemon_ucase.get_pokemons()

    return list(map(PokemonResponse.from_model, pokemons))


@router.patch('/pokemons/{no}')
async def update_pokemon(no: str, body: UpdatePokemonRequest) -> PokemonResponse:
    body.validate_pokemon_number(no)
    updated_pokemon = await pokemon_ucase.update_pokemon(no, body.to_model())

    return PokemonResponse.from_model(updated_pokemon)


@router.delete('/pokemons/{no}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon(no: str):
    await pokemon_ucase.delete_pokemon(no)
