from typing import List

from fastapi_utils.inferring_router import InferringRouter

from src import facade
from .schemas import AddEvolutionParams, CreatePokemonParams, HelloWorldNode, \
    PokemonNode, UpdatePokemonParams

router = InferringRouter(prefix="/api")


@router.get("/")
def hello() -> HelloWorldNode:
    return {"message": "Hello World"}


@router.post("/pokemon/create")
def create_pokemon(body: CreatePokemonParams) -> PokemonNode:
    return facade.add_pokemon(
        no=body.no,
        name=body.name,
        types=body.types,
    )


@router.get("/pokemon/{no}")
def get_pokemon(no: str) -> PokemonNode:
    return facade.get_pokemon(no)


@router.get("/pokemons")
def get_pokemons() -> List[PokemonNode]:
    return facade.list_pokemons()


@router.patch("/pokemon/{no}")
def update_pokemon(no: str, body: UpdatePokemonParams) -> PokemonNode:
    return facade.update_pokemon(pokemon_no=no, body=body)


@router.delete("/pokemon/{no}")
def delete_pokemon_and_evolution_relationship(no: str):
    return facade.delete_pokemon_and_evolution_relationship(pokemon_no=no)


@router.post("/pokemon/{no}/evolution")
def add_evolution(no: str, body: AddEvolutionParams) -> PokemonNode:
    return facade.add_evolution(pokemon_no=no, evolutions_no=body.evolutions_no)


@router.delete("/pokemon/{no}/evolution")
def delete_evolution(no: str, body: AddEvolutionParams):
    return facade.delete_evolution(
        pokemon_no=no, evolutions_no=body.evolutions_no
    )
