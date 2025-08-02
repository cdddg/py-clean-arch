"""
Extensions for Controller Layer.

This module provides the base schema configuration for the GraphQL API using the strawberry framework.

Note:
    For simpler requirements, use extension.py. For more complex needs, consider extensions/$package.py for better clarity and scalability.
"""

from fastapi import FastAPI


def customize_graphql_openapi(app: FastAPI) -> None:
    openapi_schema = app.openapi()
    graphql_path = '/graphql'
    if graphql_path in openapi_schema['paths']:
        openapi_schema['paths'][graphql_path]['get']['summary'] = 'GraphQL IDE access'
        openapi_schema['paths'][graphql_path]['post']['summary'] = 'Execute GraphQL Queries/Mutations'  # fmt: skip
