from typing import ClassVar
from unittest import TestCase

import pytest

from api.api_v1.movies.crud import MovieAlreadyExistsError, storage
from schemas.movies import Movie, MovieCreate, MovieUpdate, MovieUpdatePartial
from testing.conftest import create_movie


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie()

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
        cls.movies = [create_movie() for _ in range(cls.MOVIES_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies_list = storage.get()
        expected_slugs = {movie.slug for movie in self.movies}
        received_slugs = {movie.slug for movie in movies_list}

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
