import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema import Schema
from strawberry.schema.config import StrawberryConfig

from .pokemon.mutation import PokemonMutation
from .pokemon.query import PokemonQuery
from .trainer.mutation import TrainerMutation
from .trainer.query import TrainerQuery


@strawberry.type
class Query(PokemonQuery, TrainerQuery):
    pass


@strawberry.type
class Mutation(PokemonMutation, TrainerMutation):
    pass


router = GraphQLRouter(
    schema=Schema(
        query=Query,
        mutation=Mutation,
        config=StrawberryConfig(auto_camel_case=True),
    ),
)
