from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship  # type: ignore

from core.utils import build_uui4

DeclarativeMeta = declarative_base()


class Pokemon(DeclarativeMeta):
    __tablename__ = 'pokemon'

    no: Mapped[str] = Column('no', String(8), primary_key=True, comment='number')
    name: Mapped[str] = Column(String(256))
    hp = Column(Integer, nullable=True)
    attack = Column(Integer, nullable=True)
    defense = Column(Integer, nullable=True)
    sp_atk = Column(Integer, nullable=True)
    sp_def = Column(Integer, nullable=True)
    speed = Column(Integer, nullable=True)

    types = relationship('Type', secondary='pokemon_type', backref='pokemon', lazy='raise')
    before_evolutions = relationship(
        'PokemonEvolution', primaryjoin='PokemonEvolution.after_no==Pokemon.no', lazy='raise'
    )
    after_evolutions = relationship(
        'PokemonEvolution', primaryjoin='PokemonEvolution.before_no==Pokemon.no', lazy='raise'
    )


class Type(DeclarativeMeta):
    __tablename__ = 'type'

    id = Column(String(32), primary_key=True, default=build_uui4)
    name = Column(String(256))


class PokemonType(DeclarativeMeta):
    __tablename__ = 'pokemon_type'

    id = Column('id', Integer, primary_key=True)
    pokemon_no = Column(String(256), ForeignKey('pokemon.no'))
    type_id = Column(String(256), ForeignKey('type.id'))


class PokemonEvolution(DeclarativeMeta):
    __tablename__ = 'pokemon_evolution'

    id = Column(String(256), primary_key=True, default=build_uui4)
    before_no = Column(String(256), ForeignKey('pokemon.no'))
    after_no = Column(String(256), ForeignKey('pokemon.no'))

    before_pokemon = relationship(
        'Pokemon', foreign_keys=[before_no], back_populates='after_evolutions', lazy='raise'
    )
    after_pokemon = relationship(
        'Pokemon', foreign_keys=[after_no], back_populates='before_evolutions', lazy='raise'
    )
