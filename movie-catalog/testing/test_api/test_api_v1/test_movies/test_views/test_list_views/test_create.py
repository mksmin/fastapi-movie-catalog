import random
import string
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.movies import Movie, MovieCreate
from testing.conftest import build_movie_create_random_slug

pytestmark = pytest.mark.apitest


def test_create_movie(auth_client: TestClient) -> None:
    url = app.url_path_for("create_movie")
    movie_create = MovieCreate(
        title="Test Movie",
        description="Test Description",
        rating=5,
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=10,
            ),
        ),
    )
    data: dict[str, str] = movie_create.model_dump(mode="json")

    response = auth_client.post(url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    received_movie = MovieCreate(**response.json())
    assert received_movie == movie_create, response.json()


def test_create_movie_already_exists(
    auth_client: TestClient,
    movie: Movie,
) -> None:
    movie_create = MovieCreate(**movie.model_dump())
    data = movie_create.model_dump(mode="json")
    url = app.url_path_for("create_movie")
    response = auth_client.post(url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    expected_error_detail = f"Movie with slug={movie.slug!r} already exists"
    assert response.json()["detail"] == expected_error_detail, response.json()


class TestCreateInvalid:
    @pytest.fixture(
        params=[
            pytest.param(("", "string_too_short"), id="empty slug"),
            pytest.param(("ab", "string_too_short"), id="slug too short"),
            pytest.param(
                (
                    "".join(
                        random.choices(
                            string.ascii_letters,
                            k=51,
                        ),
                    ),
                    "string_too_long",
                ),
                id="slug too long",
            ),
        ],
    )
    def movie_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str]:
        build = build_movie_create_random_slug()
        data = build.model_dump(mode="json")
        slug, error_type = request.param
        data["slug"] = slug
        return data, error_type

    def test_invalid_slug(
        self,
        movie_create_values: tuple[dict[str, Any], str],
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_movie")
        data, expected_error_type = movie_create_values

        response = auth_client.post(
            url=url,
            json=data,
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == expected_error_type, error_detail
