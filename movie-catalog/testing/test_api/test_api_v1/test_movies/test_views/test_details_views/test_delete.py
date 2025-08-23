import random
import string

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.movies.crud import storage
from main import app
from schemas.movies import Movie
from testing.conftest import create_movie


@pytest.fixture(
    params=[
        "movie-slug",
        "some-slug",
        "qwerty-abc-123-!@",
        pytest.param("abc", id="minimal-slug"),
        pytest.param(
            "".join(
                random.choices(
                    string.ascii_letters,
                    k=50,
                ),
            ),
            id="max-slug",
        ),
    ],
)
def movie(request: SubRequest) -> Movie:
    return create_movie(request.param)


@pytest.mark.apitest
def test_delete(
    movie: Movie,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for(
        "delete_movie",
        movie_slug=movie.slug,
    )
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug)
