from typing import Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from core.type import UUIDStr
from core.utils import build_uui4_str

from .type import UUIDStrType


class Base(DeclarativeBase):
    pass


class Pokemon(Base):
    __tablename__ = 'pokemon'

    no: Mapped[str] = mapped_column('no', String(8), primary_key=True, comment='number')
    name: Mapped[str] = mapped_column(String(256))
    hp: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    attack: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    defense: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sp_atk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sp_def: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    speed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    types: Mapped[list['Type']] = relationship(
        'Type', secondary='pokemon_type', backref='pokemon', lazy='raise', order_by='Type.name'
    )
    before_evolutions: Mapped[list['PokemonEvolution']] = relationship(
        'PokemonEvolution',
        primaryjoin='PokemonEvolution.after_no==Pokemon.no',
        lazy='raise',
        order_by='PokemonEvolution.before_no',
    )
    after_evolutions: Mapped[list['PokemonEvolution']] = relationship(
        'PokemonEvolution',
        primaryjoin='PokemonEvolution.before_no==Pokemon.no',
        lazy='raise',
        order_by='PokemonEvolution.after_no',
    )


class Type(Base):
    __tablename__ = 'type'

    id: Mapped[UUIDStr] = mapped_column(UUIDStrType, primary_key=True, default=build_uui4_str)
    name: Mapped[str] = mapped_column(String(256))


class PokemonType(Base):
    __tablename__ = 'pokemon_type'

    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
    pokemon_no: Mapped[str] = mapped_column(String(8), ForeignKey('pokemon.no', ondelete='CASCADE'))
    type_id: Mapped[str] = mapped_column(String(32), ForeignKey('type.id'))


class PokemonEvolution(Base):
    __tablename__ = 'pokemon_evolution'

    id: Mapped[UUIDStr] = mapped_column(UUIDStrType, primary_key=True, default=build_uui4_str)
    before_no: Mapped[str] = mapped_column(String(8), ForeignKey('pokemon.no', ondelete='CASCADE'))
    after_no: Mapped[str] = mapped_column(String(8), ForeignKey('pokemon.no', ondelete='CASCADE'))
    before_pokemon: Mapped[Optional['Pokemon']] = relationship(
        'Pokemon', foreign_keys=[before_no], back_populates='after_evolutions', lazy='raise'
    )
    after_pokemon: Mapped[Optional['Pokemon']] = relationship(
        'Pokemon', foreign_keys=[after_no], back_populates='before_evolutions', lazy='raise'
    )
