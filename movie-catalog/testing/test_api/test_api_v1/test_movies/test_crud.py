import random
import string
from os import getenv
from unittest import TestCase

from api.api_v1.movies.crud import storage
from schemas.movies import Movie, MovieCreate, MovieUpdate, MovieUpdatePartial

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    raise OSError(msg)


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = self.create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def create_movie(self) -> Movie:
        movie_in = MovieCreate(
            slug="".join(random.choices(string.ascii_letters, k=10)),
            title="Test Movie",
            description="Test Description",
            rating=random.randint(1, 10),
        )
        return storage.create(movie_in)

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
