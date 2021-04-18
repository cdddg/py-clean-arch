from typing import Dict, List

from app.db import transaction
from app.models import Pokemon
from app.repositories import evolution_repo, pokemon_repo, pokemon_type_repo, \
    type_repo, evolution_relationship_repo


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
def delete_pokemon(pokemon_no: str):
    pokemon = pokemon_repo.get(pokemon_no)
    pokemon_repo.delete(pokemon_no)
    evolution_repo.delete(pokemon_id=pokemon.id)
    evolution_repo.delete(evolution_after_id=pokemon.id)

    return pokemon.to_dict()


@transaction()
def add_evolution(pokemon_no: str, evolutions: List[object]):
    origin_pokemon = pokemon_repo.get(pokemon_no)

    for row in evolutions:
        # create
        evolution_pokemon = pokemon_repo.get(row.pokemon_no)
        evolution = evolution_repo.get_or_create(
            origin_id=origin_pokemon.id,
            after_id=evolution_pokemon.id,
            _sequence=row.sequence
        )
        evolution_relationship_repo.create_or_update(
            relationship_id=origin_pokemon.relationship_id,
            evolution_id=evolution.id
        )

        # update other relationship_id to newest
        others = evolution_repo.get_pokemons(
            origin_id=origin_pokemon.id,
            after_id=evolution_pokemon.id,
        )
        relationships = evolution_relationship_repo.get_relationships(
            evolutions_id=[row.id for row in others]
        )
        evolution_relationship_repo.update_relationships_id(
            rows_id=[row.relationship_id for row in relationships],
            relationship_id=origin_pokemon.relationship_id
        )
        pokemon_repo.update_relationships_id(
            rows_id=[evolution_pokemon.relationship_id],
            relationship_id=origin_pokemon.relationship_id
        )
