from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from entrypoints.graphql.extensions.fastapi import customize_graphql_openapi
from entrypoints.graphql.pokemon.router import router as pokemon_graphql_router
from entrypoints.http.extension import add_exception_handlers as http_add_exception_handlers
from entrypoints.http.pokemon.router import router as pokemon_http_router
from settings import APP_NAME, APP_VERSION
from settings.db import IS_RELATIONAL_DB, initialize_db


# https://fastapi.tiangolo.com/advanced/events/#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=redefined-outer-name
    # pylint: disable=import-outside-toplevel

    kwargs = {}
    if IS_RELATIONAL_DB:
        from repositories.relational_db.pokemon.orm import Base  # fmt: skip
        kwargs = {'declarative_base': Base}

    await initialize_db(**kwargs)
    yield


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)
app.add_exception_handler(
    Exception,
    lambda request, exc: JSONResponse({'error': f'{type(exc).__name__}: {exc}'}, status_code=500),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# entrypoints/http
app.include_router(pokemon_http_router, tags=['HTTP'])
http_add_exception_handlers(app)

# entrypoints/graphql
app.include_router(pokemon_graphql_router, prefix='/graphql', tags=['GraphQL'])
customize_graphql_openapi(app)


@app.get('/', include_in_schema=False)
async def root():
    return JSONResponse({'service': APP_NAME, 'version': APP_VERSION})
