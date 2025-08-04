from annotated_types import (
    Len,
    Ge,
    Le,
)
from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)
from typing import Annotated

from .crud import storage
from .dependencies import get_movie_by_slug
from schemas.movies import Movie, MovieCreateSchema

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def get_movies() -> list[Movie]:
    return storage.get()


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_create: MovieCreateSchema,
) -> Movie:
    return storage.create(movie_create)


@router.get(
    "/{movie_slug}",
    response_model=Movie,
)
def get_movie(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_slug),
    ],
) -> Movie:
    return movie
