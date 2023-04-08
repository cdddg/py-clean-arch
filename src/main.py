from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from pkg.deliveries.http.pokemon.router import router as pokemon_router
from pkg.repositories.rdbms.pokemon.orm import DeclarativeMeta
from settings.db import async_engine, initialize_db

app = FastAPI()
app.add_exception_handler(
    Exception,
    lambda request, exc: JSONResponse({'error': f'{type(exc).__name__}, {exc}'}, status_code=400),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(pokemon_router)


@app.on_event('startup')
async def startup():
    await initialize_db(DeclarativeMeta, async_engine)
