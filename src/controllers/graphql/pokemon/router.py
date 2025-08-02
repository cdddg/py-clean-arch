from strawberry.fastapi import GraphQLRouter
from strawberry.schema import Schema
from strawberry.schema.config import StrawberryConfig

from .mutation import Mutation
from .query import Query

router = GraphQLRouter(
    schema=Schema(
        query=Query,
        mutation=Mutation,
        config=StrawberryConfig(auto_camel_case=True),
    ),
)
