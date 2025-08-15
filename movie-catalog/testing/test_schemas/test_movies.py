from os import getenv
from typing import Any
from unittest import TestCase

import pytest
from pydantic import ValidationError

from schemas.movies import Movie, MovieCreate, MovieUpdate, MovieUpdatePartial

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    pytest.exit(msg)


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_create_schema(self) -> None:
        data_create: dict[str, dict[str, Any]] = {
            "case1": {
                "title": "Test Movie",
                "description": "Test Description",
                "slug": "test-movie",
                "rating": 1,
            },
            "case2": {
                "title": "1",
                "description": "",
                "slug": "123",
                "rating": 10,
            },
            "case3": {
                "title": "Очень длинное название, про хоббита который нашел кольцо "
                "и живет на опушке леса",
                "description": "Очень длинное описание, про хоббита "
                "который нашел кольцо и живет на опушке леса",
                "slug": "test-movie-about-hobbit",
                "rating": "5",
            },
        }

        for case, data in data_create.items():
            with self.subTest(case=case, msg=f"test-create-{case}"):
                movie_in = MovieCreate(
                    **data,
                )
                movie = Movie(**movie_in.model_dump())
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

    def test_movie_slug_to_short(self) -> None:
        with self.assertRaises(
            ValidationError,
        ) as exc_info:

            MovieCreate(
                slug="te",
                title="Test Movie",
                description="Test Description",
                rating=1,
            )
            error_details = exc_info.exception.errors()[0]
            expected_type = "string_too_short"
            self.assertEqual(
                expected_type,
                error_details["type"],
            )

    def test_movie_slug_to_short_with_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 3 characters",
        ):

            MovieCreate(
                slug="te",
                title="Test Movie",
                description="Test Description",
                rating=1,
            )


class MovieUpdateTestCase(TestCase):
    def test_movie_can_be_updated_from_update_schema(self) -> None:
        movie = Movie(
            title="Test Movie",
            description="Test Description",
            rating=1,
            slug="test-movie",
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
        movie = Movie(
            title="Test Movie",
            description="Test Description",
            rating=1,
            slug="test-movie",
        )

        titles_for_partial_update = [
            " ",
            "Updated Movie",
            None,
            "Очень длинное название, про хоббита который нашел кольцо "
            "и живет на опушке леса",
        ]

        for title in titles_for_partial_update:
            with self.subTest(title=title, msg=f"test-partial-update-{title}"):
                movie_update = MovieUpdatePartial(title=title)
                for field, value in movie_update.model_dump(exclude_unset=True).items():
                    setattr(movie, field, value)

                self.assertEqual(
                    title,
                    movie.title,
                )
