from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.movies.crud import storage
from schemas.movies import Movie
from testing.test_api.test_api_v1.test_movies.test_crud import create_movie

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    pytest.exit(msg)


@pytest.fixture()
def movie() -> Generator[Movie, None, None]:
    movie = create_movie()
    yield movie
    storage.delete(movie)
