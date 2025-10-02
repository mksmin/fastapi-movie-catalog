from typing import ClassVar
from unittest import TestCase

import pytest

from schemas.movies import Movie, MovieCreate, MovieUpdate, MovieUpdatePartial
from storage.movies.crud import storage
from storage.movies.exceptions import MovieAlreadyExistsError
from testing.conftest import build_movie_create_random_slug, create_movie_random_slug


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie_random_slug()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def test_update(self) -> None:
        movie_in = MovieUpdate(**self.movie.model_dump())
        source_description = self.movie.description
        movie_in.description *= 2
        updated_movie = storage.update(self.movie, movie_in)

        self.assertNotEqual(
            source_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_in,
            MovieUpdate(**updated_movie.model_dump()),
        )
        self.assertEqual(
            movie_in.description,
            updated_movie.description,
        )

    def test_partial_update(self) -> None:
        movie_in = MovieUpdatePartial(
            description=self.movie.description * 2,
        )
        source_description = self.movie.description
        updated_movie = storage.update_partial(
            movie=self.movie,
            movie_in=movie_in,
        )
        self.assertNotEqual(
            source_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_in.description,
            updated_movie.description,
        )


class MovieStorageGetMoviesTestCase(TestCase):
    MOVIES_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie_random_slug() for _ in range(cls.MOVIES_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies_list = storage.get()
        expected_slugs = {movie.slug for movie in self.movies}
        received_slugs = {mv_storage.slug for mv_storage in movies_list}

        expected_diff = set[str]()
        diff = expected_slugs - received_slugs

        self.assertEqual(
            expected_diff,
            diff,
        )

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Validate can be slug={movie.slug!r}",
            ):
                db_movie = storage.get_by_slug(movie.slug)
                self.assertEqual(
                    movie,
                    db_movie,
                )


def test_create_or_raise_if_exists(movie: Movie) -> None:
    movie_in = MovieCreate(**movie.model_dump())
    with pytest.raises(
        MovieAlreadyExistsError,
        match=movie_in.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(
            movie_in=movie_in,
        )

    assert exc_info.value.args[0] == movie_in.slug


def test_create_twice() -> None:
    movie_create = build_movie_create_random_slug()
    # create new movie successfully
    storage.create_or_raise_if_exists(movie_create)
    # create second time, raises
    with pytest.raises(
        MovieAlreadyExistsError,
        match=movie_create.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(movie_create)
    assert exc_info.value.args == (movie_create.slug,)
