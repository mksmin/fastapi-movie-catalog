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


def build_movie_create(slug: str) -> MovieCreate:
    return MovieCreate(
        title="Test Movie",
        description="Test Description",
        rating=5,
        slug=slug,
    )


def build_movie_create_random_slug() -> MovieCreate:
    return build_movie_create(
        slug="".join(
            random.choices(  # noqa: S311
                string.ascii_letters,
                k=10,
            ),
        ),
    )


def create_movie(slug: str) -> Movie:
    movie_in = build_movie_create(slug)
    return storage.create(movie_in)


def create_movie_random_slug() -> Movie:
    movie_in = build_movie_create_random_slug
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie, None, None]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
