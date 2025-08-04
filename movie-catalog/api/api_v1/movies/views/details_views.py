from fastapi import (
    APIRouter,
    Depends,
    status,
)
from typing import Annotated

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import get_movie_by_slug
from schemas.movies import Movie

router = APIRouter(
    prefix="/{movie_slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie 'movie_slug' not found",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=Movie,
)
def get_movie(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_slug),
    ],
) -> Movie:
    return movie


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_slug),
    ],
) -> None:
    storage.delete(movie)
