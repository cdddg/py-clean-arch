from typing import Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from common.type import PokemonNumberStr, UUIDStr
from common.utils import build_uuid4_str


class Base(DeclarativeBase):
    pass


class Pokemon(Base):
    __tablename__ = 'pokemon'

    no: Mapped[PokemonNumberStr] = mapped_column(
        String(8), primary_key=True, comment='pokemon number'
    )
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
    previous_evolutions: Mapped[list['PokemonEvolution']] = relationship(
        'PokemonEvolution',
        primaryjoin='PokemonEvolution.next_no==Pokemon.no',
        lazy='raise',
        order_by='PokemonEvolution.previous_no',
    )
    next_evolutions: Mapped[list['PokemonEvolution']] = relationship(
        'PokemonEvolution',
        primaryjoin='PokemonEvolution.previous_no==Pokemon.no',
        lazy='raise',
        order_by='PokemonEvolution.next_no',
    )


class Type(Base):
    __tablename__ = 'type'

    id: Mapped[UUIDStr] = mapped_column(String(32), primary_key=True, default=build_uuid4_str)
    name: Mapped[str] = mapped_column(String(256))


class PokemonType(Base):
    __tablename__ = 'pokemon_type'

    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
    pokemon_no: Mapped[PokemonNumberStr] = mapped_column(
        String(8), ForeignKey(f'{Pokemon.__tablename__}.no', ondelete='CASCADE')
    )
    type_id: Mapped[str] = mapped_column(String(32), ForeignKey('type.id'))


class PokemonEvolution(Base):
    __tablename__ = 'pokemon_evolution'

    id: Mapped[UUIDStr] = mapped_column(String(32), primary_key=True, default=build_uuid4_str)
    previous_no: Mapped[PokemonNumberStr] = mapped_column(
        String(8), ForeignKey(f'{Pokemon.__tablename__}.no', ondelete='CASCADE')
    )
    next_no: Mapped[PokemonNumberStr] = mapped_column(
        String(8), ForeignKey(f'{Pokemon.__tablename__}.no', ondelete='CASCADE')
    )
    previous_pokemon: Mapped[Optional['Pokemon']] = relationship(
        'Pokemon', foreign_keys=[previous_no], back_populates='next_evolutions', lazy='raise'
    )
    next_pokemon: Mapped[Optional['Pokemon']] = relationship(
        'Pokemon', foreign_keys=[next_no], back_populates='previous_evolutions', lazy='raise'
    )
