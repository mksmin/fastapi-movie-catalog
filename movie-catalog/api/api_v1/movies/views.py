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

from .crud import MOVIES
from .dependencies import get_movie_by_id
from schemas.movies import Movie, MovieCreateSchema

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def get_movies():
    return MOVIES


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_create: MovieCreateSchema,
):
    return Movie(
        **movie_create.dict(),
    )


@router.get(
    "/{movie_slug}",
    response_model=Movie,
)
def get_movie(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_id),
    ],
):
    return movie
