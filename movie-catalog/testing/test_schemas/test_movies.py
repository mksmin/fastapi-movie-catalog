from schemas.movies import Movie, MovieCreate
from unittest import TestCase


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_create_schema(self) -> None:
        movie_in = MovieCreate(
            title="Test Movie",
            description="Test Description",
            rating=1,
            slug="test-movie",
        )

        movie = Movie(
            **movie_in.model_dump(),
        )
        self.assertEqual(
            movie_in.description,
            movie.description,
        )
        self.assertEqual(
            movie_in.title,
            movie.title,
        )
        self.assertEqual(
            movie_in.rating,
            movie.rating,
        )
        self.assertEqual(
            movie_in.slug,
            movie.slug,
        )
