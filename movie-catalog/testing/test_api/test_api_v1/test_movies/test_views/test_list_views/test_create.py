import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.movies import Movie, MovieCreate


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
