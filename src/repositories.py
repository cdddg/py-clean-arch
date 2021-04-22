from typing import List

from src.db import get_session
from src.exceptions import PokemonNotFound, PokemonUnknownError
from src.models import Evolution, Pokemon, PokemonType, Type


class BaseRepository:
    MODEL_CLS = None

    @property
    def _session(self):
        return get_session()

    def add(self, entity):
        try:
            self._session.add(entity)
            self._session.flush()
            return entity
        except Exception as e:
            raise PokemonUnknownError(e)


class PokemonRepository(BaseRepository):
    MODEL_CLS = Pokemon

    def get(self, pokemon_no: str):
        try:
            return (
                self._session.query(self.MODEL_CLS)
                .filter_by(no=pokemon_no)
                .one()
            )
        except Exception as e:
            raise PokemonNotFound(e)

    def filter(self, pokemons_no):
        return self._session.query(self.MODEL_CLS).filter(
            self.MODEL_CLS.no.in_(pokemons_no)
        )

    def list(self):
        return (
            self._session.query(self.MODEL_CLS)
            .order_by(self.MODEL_CLS.no)
            .all()
        )

    def update_relationships_id(self, rows_id: List[str], relationship_id: str):
        return (
            self._session.query(self.MODEL_CLS)
            .filter(self.MODEL_CLS.relationship_id.in_(rows_id))
            .update(dict(relationship_id=relationship_id))
        )

    def delete(self, pokemon_no: str):
        return (
            self._session.query(self.MODEL_CLS)
            .filter_by(no=pokemon_no)
            .delete()
        )


class TypeRepository(BaseRepository):
    MODEL_CLS = Type

    def get_or_create(self, name: str):
        type_ = (
            self._session.query(self.MODEL_CLS)
            .filter_by(name=name)
            .one_or_none()
        )
        if not type_:
            type_ = self.MODEL_CLS(name=name)
            self.add(type_)
        return type_


class PokemonTypeRepository(BaseRepository):
    MODEL_CLS = PokemonType

    def find(self, id: str):
        return self._session.query(self.MODEL_CLS).filter_by(id=id).all()

    def delete(self, pokemon_id: str):
        return (
            self._session.query(self.MODEL_CLS)
            .filter_by(pokemon_id=pokemon_id)
            .delete()
        )


class EvolutionRepository(BaseRepository):
    MODEL_CLS = Evolution

    def get_or_create(self, before_id: str, after_id: str):
        pokemon = (
            self._session.query(self.MODEL_CLS)
            .filter_by(before_id=before_id, after_id=after_id)
            .one_or_none()
        )
        if not pokemon:
            pokemon = self.add(
                self.MODEL_CLS(
                    before_id=before_id,
                    after_id=after_id,
                )
            )

        return pokemon

    def delete_before_pokemon(self, before_id: str):
        return (
            self._session.query(self.MODEL_CLS)
            .filter_by(before_id=before_id)
            .delete()
        )

    def delete_after_pokemon(self, after_id: str):
        return (
            self._session.query(self.MODEL_CLS)
            .filter_by(after_id=after_id)
            .delete()
        )


pokemon_repo = PokemonRepository()
type_repo = TypeRepository()
pokemon_type_repo = PokemonTypeRepository()
evolution_repo = EvolutionRepository()
