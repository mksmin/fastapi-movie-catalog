from fastapi import (
    Depends,
    APIRouter,
)
from typing import Annotated

from .crud import MOVIES
from .dependencies import get_movie_by_id
from schemas.movies import Movie

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


@router.get(
    "/{movie_id}",
    response_model=Movie,
)
def get_movie(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_id),
    ],
):
    return movie
