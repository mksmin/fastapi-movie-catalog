from typing import Annotated

from fastapi import Depends

from core.config import settings
from storage.movies import MovieStorage


def get_movies_storage() -> MovieStorage:
    return MovieStorage(
        hash_name=settings.redis.collections_names.movie_hash,
    )


GetMoviesStorage = Annotated[
    MovieStorage,
    Depends(get_movies_storage),
]
