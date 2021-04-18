from sqlalchemy import or_
from typing import List
from app.db import get_session
from app.exceptions import PokemonNotFound, PokemonUnknownError
from app.models import Evolution, Pokemon, PokemonType, Type, EvolutionRelationship


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

    def get(self, pokemon_no):
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

    def update_relationships_id(self, rows_id, relationship_id):
        return self._session.query(self.MODEL_CLS).filter(
            self.MODEL_CLS.relationship_id.in_(rows_id)
        ).update(
            dict(relationship_id=relationship_id)
        )

    def delete(self, pokemon_no):
        return (
            self._session.query(self.MODEL_CLS)
            .filter_by(no=pokemon_no)
            .delete()
        )


class TypeRepository(BaseRepository):

    MODEL_CLS = Type

    def get_or_create(self, name):
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

    def find(self, id):
        return self._session.query(self.MODEL_CLS).filter_by(id=id).all()

    def delete(self, pokemon_id):
        return (
            self._session.query(self.MODEL_CLS)
            .filter_by(pokemon_id=pokemon_id)
            .delete()
        )


class EvolutionRepository(BaseRepository):

    MODEL_CLS = Evolution

    def get_or_create(self, origin_id, after_id, _sequence):
        pokemon = self._session.query(self.MODEL_CLS).filter_by(origin_id=origin_id, after_id=after_id).one_or_none()
        if not pokemon:
            pokemon = self.add(
                self.MODEL_CLS(
                    origin_id=origin_id,
                    after_id=after_id,
                    sequence=_sequence,
                )
            )

        return pokemon

    def get_pokemons(self, origin_id, after_id):
        return (
            self._session.query(self.MODEL_CLS)
            .filter(
                or_(
                    self.MODEL_CLS.after_id == origin_id,
                    self.MODEL_CLS.origin_id == after_id,
                )
            )
            .all()
        )


class EvolutionRelationshipRepository(BaseRepository):

    MODEL_CLS = EvolutionRelationship

    def create_or_update(self, relationship_id, evolution_id):
        relationship = self._session.query(self.MODEL_CLS) \
            .filter_by(evolution_id=evolution_id) \
            .one_or_none()
        if not relationship:
            relationship = self.add(
                self.MODEL_CLS(
                    relationship_id=relationship_id,
                    evolution_id=evolution_id
                )
            )
        else:
            relationship.relationship_id = relationship_id

        return relationship

    def get_relationships(self, evolutions_id: List[str]):
        return self._session.query(self.MODEL_CLS).filter(
            self.MODEL_CLS.evolution_id.in_(evolutions_id)
        ).all()

    def update_relationship_id(self, rows_id, relationship_id):
        return self._session.query(self.MODEL_CLS).filter(
            self.MODEL_CLS.relationship_id.in_(rows_id)
        ).update(
            dict(relationship_id=relationship_id)
        )

    def delete(self, **kwargs):
        return self._session.query(self.MODEL_CLS).filter_by(**kwargs).delete()


pokemon_repo = PokemonRepository()
type_repo = TypeRepository()
pokemon_type_repo = PokemonTypeRepository()
evolution_repo = EvolutionRepository()
evolution_relationship_repo = EvolutionRelationshipRepository()
