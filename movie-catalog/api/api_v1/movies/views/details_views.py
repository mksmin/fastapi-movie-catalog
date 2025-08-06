from fastapi import (
    APIRouter,
    Depends,
    status,
)
from typing import Annotated

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import get_movie_by_slug
from schemas.movies import (
    Movie,
    MovieUpdate,
    MovieUpdatePartial,
    MovieRead,
)

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

MovieBySlug = Annotated[
    Movie,
    Depends(get_movie_by_slug),
]


@router.get(
    "/",
    response_model=MovieRead,
)
def get_movie(
    movie: MovieBySlug,
) -> Movie:
    return movie


@router.put(
    "/",
    response_model=MovieRead,
)
def update_movie(
    movie: MovieBySlug,
    movie_in: MovieUpdate,
) -> Movie:
    return storage.update(
        movie=movie,
        movie_in=movie_in,
    )


@router.patch(
    "/",
    response_model=MovieRead,
)
def update_movie_partial(
    movie: MovieBySlug,
    movie_in: MovieUpdatePartial,
) -> Movie:
    return storage.update_partial(
        movie=movie,
        movie_in=movie_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: MovieBySlug,
) -> None:
    storage.delete(movie)
