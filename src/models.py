from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .core.utils import build_uui4

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(String(32), primary_key=True, default=build_uui4)
    no = Column(String(32), index=True, unique=True, comment="number")
    name = Column(String(256))
    hp = Column(Integer, nullable=True)
    attack = Column(Integer, nullable=True)
    defense = Column(Integer, nullable=True)
    sp_atk = Column(Integer, nullable=True)
    sp_def = Column(Integer, nullable=True)
    speed = Column(Integer, nullable=True)

    types = relationship("Type", secondary="pokemon_type", backref="pokemon")
    before_evolutions = relationship(
        "Evolution", primaryjoin="Evolution.after_id==Pokemon.id"
    )
    after_evolutions = relationship(
        "Evolution", primaryjoin="Evolution.before_id==Pokemon.id"
    )

    @property
    def data(self):
        return {
            "id": self.id,
            "no": self.no,
            "name": self.name,
        }

    def to_dict(self):
        data = self.data
        data["types"] = [{"id": row.id, "name": row.name} for row in self.types]
        data["evolutions"] = {
            "before": [
                row.before_pokemon.data for row in self.before_evolutions
            ],
            "after": [row.after_pokemon.data for row in self.after_evolutions],
        }
        return data


class Type(Base):
    __tablename__ = "type"

    id = Column(String(32), primary_key=True, default=build_uui4)
    name = Column(String(256))


class PokemonType(Base):
    __tablename__ = "pokemon_type"

    id = Column("id", Integer, primary_key=True)
    pokemon_id = Column(String(256), ForeignKey("pokemon.id"))
    type_id = Column(String(256), ForeignKey("type.id"))


class Evolution(Base):
    __tablename__ = "evolution"

    id = Column(String(256), primary_key=True, default=build_uui4)
    before_id = Column(String(256), ForeignKey("pokemon.id"))
    after_id = Column(String(256), ForeignKey("pokemon.id"))

    before_pokemon = relationship(
        "Pokemon", foreign_keys=[before_id], back_populates="after_evolutions"
    )
    after_pokemon = relationship(
        "Pokemon", foreign_keys=[after_id], back_populates="before_evolutions"
    )
