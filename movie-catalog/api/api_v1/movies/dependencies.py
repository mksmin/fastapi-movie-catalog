import random

from fastapi import HTTPException, status

from .crud import storage
from schemas.movies import Movie


def get_movie_by_slug(
    movie_slug: str,
):
    movie: Movie | None = storage.get_by_slug(slug=movie_slug)

    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {movie_slug!r} not found",
    )
