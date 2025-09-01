import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.movies.crud import storage
from schemas.movies import Movie, MovieCreate


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        msg = "Environment is not ready for testing"
        pytest.exit(msg)


def build_movie_create(
    slug: str,
    title: str = "Test Movie",
    description: str = "Test Movie Description",
    rating: int = 5,
) -> MovieCreate:
    return MovieCreate(
        title=title,
        description=description,
        rating=rating,
        slug=slug,
    )


def build_movie_create_random_slug(
    title: str = "Test Movie",
    description: str = "Test Movie Description",
    rating: int = 5,
) -> MovieCreate:
    return build_movie_create(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=10,
            ),
        ),
        title=title,
        description=description,
        rating=rating,
    )


def create_movie(
    slug: str,
    title: str = "Test Movie",
    description: str = "Test Movie Description",
    rating: int = 5,
) -> Movie:
    movie_in = build_movie_create(
        slug=slug,
        title=title,
        description=description,
        rating=rating,
    )
    return storage.create(movie_in)


def create_movie_random_slug(
    title: str = "Test Movie",
    description: str = "Test Movie Description",
    rating: int = 5,
) -> Movie:
    movie_in = build_movie_create_random_slug(
        title=title,
        description=description,
        rating=rating,
    )
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie, None, None]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
