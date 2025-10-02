from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.movies import DESCRIPTION_MAX_LENGTH, Movie
from storage.movies.crud import storage
from testing.conftest import create_movie_random_slug


@pytest.mark.apitest
class TestUpdatePartial:
    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie, None, None]:
        movie = create_movie_random_slug(
            description=request.param,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param(
                "some description",
                "",
                id="some-description-to-no-description",
            ),
            pytest.param(
                "",
                "some description",
                id="no-description-to-some-description",
            ),
            pytest.param(
                "",
                "a" * DESCRIPTION_MAX_LENGTH,
                id="min-description-to-max-description",
            ),
            pytest.param(
                "a" * DESCRIPTION_MAX_LENGTH,
                "",
                id="min-description-to-max-description",
            ),
        ],
        indirect=["movie"],
    )
    def test_movie_update_partial(
        self,
        movie: Movie,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("update_movie_partial", movie_slug=movie.slug)
        response = auth_client.patch(
            url,
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        assert movie_db.description == new_description
