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
    HTTPBasic,
    HTTPBasicCredentials,
)

from core.config import (
    REDIS_API_TOKENS_SET_NAME,
    USERS_DB,
)
from .crud import storage
from .redis import redis
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
user_basic_auth = HTTPBasic(
    scheme_name="User Basic Auth",
    description="Use username and password to authenticate. [Read more](https://ya.ru)",
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


def validate_api_token(
    api_token: HTTPAuthorizationCredentials | None,
):

    if redis.sismember(
        name=REDIS_API_TOKENS_SET_NAME,
        value=api_token.credentials,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API token",
    )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(
            static_api_token,
        ),
    ] = None,
) -> None:
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )

    validate_api_token(
        api_token=api_token,
    )


def validate_user_credentials(
    credentials: HTTPBasicCredentials | None,
):
    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):

    validate_user_credentials(
        credentials=credentials,
    )


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(
            static_api_token,
        ),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if api_token:
        return validate_api_token(api_token=api_token)
    if credentials:
        return validate_user_credentials(credentials=credentials)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth are required.",
    )
