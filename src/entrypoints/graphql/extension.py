"""
Extensions for Entrypoint Layer.

This module provides the base schema configuration for the GraphQL API using the strawberry framework.

Note:
    For simpler requirements, use extension.py. For more complex needs, consider extensions/$package.py for better clarity and scalability.
"""

from fastapi import FastAPI


def customize_graphql_openapi(app: FastAPI) -> None:
    openapi_schema = app.openapi()
    if '/graphql' in openapi_schema['paths']:
        openapi_schema['paths']['/graphql']['get']['summary'] = 'GraphQL IDE access'
        openapi_schema['paths']['/graphql']['post']['summary'] = 'Execute GraphQL Queries/Mutations'
