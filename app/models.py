from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .core.utils import build_uui4

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(String, primary_key=True, default=build_uui4)
    no = Column(String, index=True, unique=True, comment="number")
    name = Column(String)
    relationship_id = Column(String, default=build_uui4)
    # hp = Column(Integer, nullable=True)
    # attack = Column(Integer, nullable=True)
    # defense = Column(Integer, nullable=True)
    # sp_atk = Column(Integer, nullable=True)
    # sp_def = Column(Integer, nullable=True)
    # speed = Column(Integer, nullable=True)

    types = relationship("Type", secondary="pokemon_type", backref="pokemon")
    # evolutions = relationship(
    #     "Evolution",
    #     primaryjoin="Pokemon.evolution_group_id==Evolution.group_id",
    #     order_by="Evolution.serial",
    # )

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
        data["evolutions"] = []

        return data


class Type(Base):
    __tablename__ = "type"

    id = Column(String, primary_key=True, default=build_uui4)
    name = Column(String)


class PokemonType(Base):
    __tablename__ = "pokemon_type"

    id = Column("id", Integer, primary_key=True)
    pokemon_id = Column(String, ForeignKey("pokemon.id"))
    type_id = Column(String, ForeignKey("type.id"))


class Evolution(Base):
    __tablename__ = "evolution"

    id = Column(String, primary_key=True, default=build_uui4)
    origin_id = Column(String, ForeignKey("pokemon.id", ondelete="CASCADE"))
    after_id = Column(String, ForeignKey("pokemon.id", ondelete="CASCADE"))
    sequence = Column(Integer)


class EvolutionRelationship(Base):
    __tablename__ = "evolution_relationship"

    id = Column(Integer, primary_key=True)
    relationship_id = Column(String)
    evolution_id = Column(String, ForeignKey("evolution.id", ondelete="CASCADE"))
