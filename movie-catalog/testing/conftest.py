import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.movies.crud import storage
from schemas.movies import Movie, MovieCreate

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    pytest.exit(msg)


def create_movie() -> Movie:
    movie_in = MovieCreate(
        slug="".join(
            random.choices(  # noqa: S311
                string.ascii_letters,
                k=10,
            ),
        ),
        title="Test Movie",
        description="Test Description",
        rating=random.randint(1, 10),  # noqa: S311
    )
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie, None, None]:
    movie = create_movie()
    yield movie
    storage.delete(movie)
