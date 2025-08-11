from schemas.movies import Movie, MovieCreate, MovieUpdate, MovieUpdatePartial
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


class MovieUpdateTestCase(TestCase):
    def test_movie_can_be_updated_from_update_schema(self) -> None:
        movie_in = MovieCreate(
            title="Test Movie",
            description="Test Description",
            rating=1,
            slug="test-movie",
        )

        movie = Movie(
            **movie_in.model_dump(),
        )

        movie_update = MovieUpdate(
            title="Updated Movie",
            description="Updated Description",
            rating=2,
        )
        for field, value in movie_update.model_dump().items():
            setattr(movie, field, value)

        self.assertEqual(
            movie_update.title,
            movie.title,
        )
        self.assertEqual(
            movie_update.description,
            movie.description,
        )
        self.assertEqual(
            movie_update.rating,
            movie.rating,
        )


class MoviePartialUpdateTestCase(TestCase):
    def test_movie_can_be_updated_from_partial_update_schema(self) -> None:
        movie_in = MovieCreate(
            title="Test Movie",
            description="Test Description",
            rating=1,
            slug="test-movie",
        )
        movie = Movie(
            **movie_in.model_dump(),
        )

        movie_update = MovieUpdatePartial(
            title="Updated Movie",
        )
        for field, value in movie_update.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        self.assertEqual(
            movie_update.title,
            movie.title,
        )

        movie_update = MovieUpdatePartial(
            description="",
        )
        for field, value in movie_update.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        self.assertEqual(
            movie_update.description,
            movie.description,
        )

        movie_update = MovieUpdatePartial(
            rating=3,
        )
        for field, value in movie_update.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        self.assertEqual(
            movie_update.rating,
            movie.rating,
        )
