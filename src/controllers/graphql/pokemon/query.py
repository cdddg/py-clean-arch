from typing import Annotated

import strawberry
from strawberry.types import Info

import usecases.pokemon as pokemon_ucase
from common.type import PokemonNumberStr
from di.dependency_injection import injector
from di.unit_of_work import AbstractUnitOfWork

from .mapper import PokemonNodeMapper
from .schema import PokemonNode


@strawberry.type
class Query:
    """
    GraphQL Performance Optimization Notes.

    Current Implementation Limitation:
    The current GraphQL resolvers load all relational data (types, evolutions) regardless of
    which fields are actually requested in the query. This defeats the purpose of GraphQL's
    selective field querying capability.

    For example, a query like:
      query { pokemon(no: "001") { no, name } }
    Still triggers database queries for types and evolutions that aren't needed.

    Potential Optimization Strategies:

    1. Field Selection Analysis
       - Parse the GraphQL Info parameter to determine requested fields
       - Implement conditional loading in usecases based on field selection
       - Modify repository layer to support selective data loading

    2. DataLoader Pattern
       - Implement batched loading for relational data to solve N+1 query problems
       - Use lazy loading in GraphQL resolvers with proper caching

    3. Dedicated GraphQL Usecases
       - Create GraphQL-specific usecases that don't impact REST API compatibility
       - Maintain separation of concerns between different API layers

    4. Repository Method Specialization
       - Provide multiple query methods (minimal, with_types, full)
       - Allow resolvers to choose appropriate data loading strategy

    Implementation Priority: High for field selection analysis, Medium for DataLoader pattern.
    """

    @strawberry.field
    async def pokemons(self, _: Info) -> list[PokemonNode]:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        pokemons = await pokemon_ucase.get_pokemons(async_unit_of_work)

        return list(map(PokemonNodeMapper.entity_to_node, pokemons))

    @strawberry.field
    async def pokemon(
        self,
        no: Annotated[str, strawberry.argument(description=PokemonNumberStr.__doc__)],
        _: Info,
    ) -> PokemonNode:
        async_unit_of_work = injector.get(AbstractUnitOfWork)
        no = PokemonNumberStr(no)
        pokemon = await pokemon_ucase.get_pokemon(async_unit_of_work, no)

        return PokemonNodeMapper.entity_to_node(pokemon)
