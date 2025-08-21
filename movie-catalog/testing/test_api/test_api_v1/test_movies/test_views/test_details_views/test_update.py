from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.movies.crud import storage
from main import app
from schemas.movies import DESCRIPTION_MAX_LENGTH, TITLE_MAX_LENGTH, Movie, MovieUpdate
from testing.conftest import create_movie_random_slug


class TestUpdate:
    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie, None, None]:
        title, description, rating = request.param
        movie = create_movie_random_slug(
            title=title,
            description=description,
            rating=rating,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_title, new_description, new_rating",
        [
            pytest.param(
                ("a", "", 1),
                "a" * TITLE_MAX_LENGTH,
                "b" * DESCRIPTION_MAX_LENGTH,
                10,
                id="min-params-to-max-params",
            ),
            pytest.param(
                ("a" * TITLE_MAX_LENGTH, "b" * DESCRIPTION_MAX_LENGTH, 10),
                "a",
                "",
                1,
                id="max-params-to-min-params",
            ),
            pytest.param(
                ("Some title", "Some description", 5),
                "New title",
                "New description",
                8,
                id="some-params-to-new-params",
            ),
            pytest.param(
                ("Greate movie", "Big surprise", 10),
                "Greate movie",
                "",
                8,
                id="same-title-to-no-description",
            ),
        ],
        indirect=["movie"],
    )
    def test_movie_update_details(
        self,
        movie: Movie,
        new_title: str,
        new_description: str,
        new_rating: int,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("update_movie", movie_slug=movie.slug)
        update = MovieUpdate(
            title=new_title,
            description=new_description,
            rating=new_rating,
        )
        response = auth_client.put(
            url,
            json=update.model_dump(mode="json"),
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        new_data = MovieUpdate(**movie_db.model_dump())
        assert new_data == update
