from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.db import get_engine
from src.models import Base
from src.routers import apis
from src.routers.schemas import HTTPBadRequest

Base.metadata.create_all(get_engine())


app = FastAPI(
    responses={400: {"model": HTTPBadRequest}},
)

app.add_exception_handler(
    Exception,
    lambda request, exc: JSONResponse(
        {"error": f"{type(exc).__name__}, {exc}"}, status_code=400
    ),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(apis.router)
