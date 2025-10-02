from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from storage.movies import MovieStorage


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncIterator[None]:
    app.state.movies_storage = MovieStorage(
        hash_name=settings.redis.collections_names.movie_hash,
    )
    yield
