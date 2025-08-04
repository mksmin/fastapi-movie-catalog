import random

from fastapi import HTTPException, status

from .crud import MOVIES
from schemas.movies import Movie


def get_movie_by_id(
    movie_slug: str,
):
    movie: Movie | None = next(
        (movie for movie in MOVIES if movie.slug == movie_slug),
        None,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Movie not found",
    )
