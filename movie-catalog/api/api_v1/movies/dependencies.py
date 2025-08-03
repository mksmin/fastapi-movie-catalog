from fastapi import HTTPException, status

from .crud import MOVIES
from schemas.movies import Movie


def get_movie_by_id(
    movie_id: int,
):
    movie: Movie | None = next(
        (movie for movie in MOVIES if movie.id == movie_id),
        None,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Movie not found",
    )
