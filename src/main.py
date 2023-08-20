from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.deliveries.graphql.pokemon.router import router as pokemon_graphql_router
from app.deliveries.http.fastapi import add_exception_handlers as http_add_exception_handlers
from app.deliveries.http.pokemon.router import router as pokemon_http_router
from app.repositories.rdbms.pokemon.orm import Base
from settings import APP_NAME, APP_VERSION
from settings.db import AsyncEngine, initialize_db

app = FastAPI(title=APP_NAME, version=APP_VERSION)
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

# deliveries/http
app.include_router(pokemon_http_router, tags=['HTTP'])
http_add_exception_handlers(app)

# deliveries/graphql
app.include_router(pokemon_graphql_router, prefix='/graphql', tags=['GraphQL'])


@app.on_event('startup')
async def startup():
    await initialize_db(Base, AsyncEngine)


@app.get('/', include_in_schema=False)
async def root():
    return JSONResponse({'service': APP_NAME, 'version': APP_VERSION})
