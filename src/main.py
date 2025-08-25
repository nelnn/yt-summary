"""Main entrypoint."""

import logging

import fastapi
from fastapi.middleware import cors
from fastapi.staticfiles import StaticFiles

from src.api.router import router
from src.config import settings

logger = logging.getLogger(__name__)


app = fastapi.FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
