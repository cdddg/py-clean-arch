from typing import Dict, List

from app.db import transaction
from app.models import Pokemon
from app.repositories import evolution_repo, pokemon_repo, pokemon_type_repo, \
    type_repo


@transaction()
def add_pokemon(no: int, name: str, types: List[str]) -> Dict:
    pokemon = Pokemon(id=no, no=no, name=name)
    pokemon.types = [type_repo.get_or_create(t) for t in types]
    return pokemon_repo.add(pokemon).to_dict()


def get_pokemon(pokemon_no: str):
    return pokemon_repo.get(pokemon_no).to_dict()


def list_pokemons():
    return [pokemon.to_dict() for pokemon in pokemon_repo.list()]


@transaction()
def update_pokemon(pokemon_no: str, body: object):
    pokemon = pokemon_repo.get(pokemon_no)
    if body.name:
        pokemon.name = body.name
    if body.types:
        pokemon_type_repo.delete(pokemon_id=pokemon.id)
        pokemon.types = [type_repo.get_or_create(t) for t in body.types]

    return pokemon.to_dict()


@transaction()
def delete_pokemon_and_evolution_relationship(pokemon_no: str):
    pokemon = pokemon_repo.get(pokemon_no)
    pokemon_repo.delete(pokemon_no)
    evolution_repo.delete_before_pokemon(pokemon.id)
    evolution_repo.delete_after_pokemon(pokemon.id)

    return pokemon.to_dict()


@transaction()
def add_evolution(pokemon_no: str, evolutions_no: List[str]):
    origin_pokemon = pokemon_repo.get(pokemon_no)

    for no in evolutions_no:
        evolution_pokemon = pokemon_repo.get(no)
        evolution_repo.get_or_create(
            before_id=origin_pokemon.id, after_id=evolution_pokemon.id
        )

    return origin_pokemon.to_dict()
