from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.type import UUIDStr
from common.utils import build_uuid4_str

from ..base import Base
from ..pokemon.orm import Pokemon


class Trainer(Base):
    __tablename__ = 'trainer'

    id: Mapped[UUIDStr] = mapped_column(String(32), primary_key=True, default=build_uuid4_str)
    name: Mapped[str] = mapped_column(String(256))
    region: Mapped[str] = mapped_column(String(256))
    badge_count: Mapped[int] = mapped_column(Integer, default=0)

    team: Mapped[list['TrainerPokemon']] = relationship(
        'TrainerPokemon',
        back_populates='trainer',
        lazy='raise',
        cascade='all, delete-orphan',
        order_by='TrainerPokemon.pokemon_no',
    )


class TrainerPokemon(Base):
    __tablename__ = 'trainer_pokemon'

    id: Mapped[int] = mapped_column('id', Integer, primary_key=True)
    trainer_id: Mapped[UUIDStr] = mapped_column(
        String(32), ForeignKey('trainer.id', ondelete='CASCADE')
    )
    pokemon_no: Mapped[str] = mapped_column(String(8), ForeignKey('pokemon.no', ondelete='CASCADE'))

    trainer: Mapped['Trainer'] = relationship('Trainer', back_populates='team', lazy='raise')
    pokemon: Mapped['Pokemon'] = relationship('Pokemon', lazy='raise')
