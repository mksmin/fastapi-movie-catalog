from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    Request,
    status,
)

from schemas.movies import Movie
from storage.movies import MovieStorage


def get_movies_storage(
    request: Request,
) -> MovieStorage:
    return request.app.state.movies_storage  # type: ignore[no-any-return]


GetMoviesStorage = Annotated[
    MovieStorage,
    Depends(get_movies_storage),
]


def get_movie_by_slug(
    slug: str,
    storage: GetMoviesStorage,
) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug=slug)

    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found",
    )


MovieBySlug = Annotated[
    Movie,
    Depends(get_movie_by_slug),
]
