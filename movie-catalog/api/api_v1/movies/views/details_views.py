from fastapi import (
    APIRouter,
    status,
)

from dependencies.movies import MovieBySlug
from schemas.movies import (
    Movie,
    MovieRead,
    MovieUpdate,
    MovieUpdatePartial,
)
from storage.movies.crud import storage

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


@router.post(
    "transfer",
)
def transfer_movie(
    # movie: Movie,
) -> None:
    # something here
    raise NotImplementedError
