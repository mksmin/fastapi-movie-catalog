import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.movies import MovieCreate


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
