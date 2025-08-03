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
from .dependencies import get_movie_by_id, set_movie_id
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


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_id: Annotated[int, Depends(set_movie_id)],
    title: Annotated[
        str,
        Len(min_length=5, max_length=100),
        Form(),
    ],
    description: Annotated[
        str,
        Len(min_length=10, max_length=250),
        Form(),
    ],
    rating: Annotated[
        int,
        Ge(1),
        Le(10),
        Form(),
    ],
):
    return Movie(
        id=movie_id,
        title=title,
        description=description,
        rating=rating,
    )


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
