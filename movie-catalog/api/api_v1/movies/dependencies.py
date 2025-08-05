import logging
from fastapi import HTTPException, status, BackgroundTasks

from .crud import storage
from schemas.movies import Movie

log = logging.getLogger(__name__)


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


def storage_save_state(
    background_tasks: BackgroundTasks,
):
    yield
    log.info("Saving state in background")
    background_tasks.add_task(storage.save_state)
