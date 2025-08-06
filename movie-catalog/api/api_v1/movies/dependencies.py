import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    status,
    BackgroundTasks,
    Request,
    Depends,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from core.config import API_TOKENS
from .crud import storage
from schemas.movies import Movie

log = logging.getLogger(__name__)
UNSAFE_METHODS = frozenset(
    {
        "DELETE",
        "PATCH",
        "PUT",
        "POST",
    }
)
static_api_token = HTTPBearer(
    scheme_name="Static API Token",
    description="Your **Static API token** from the developer portal. [Read more](https://ya.ru)",
    auto_error=False,
)


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
    request: Request,
):
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Saving state in background")
        background_tasks.add_task(storage.save_state)


def api_token_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(
            static_api_token,
        ),
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API token",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API token",
        )
