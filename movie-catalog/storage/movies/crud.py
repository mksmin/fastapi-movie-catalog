__all__ = (
    "MovieStorage",
    "storage",
)


import logging
from collections.abc import Iterable
from typing import cast

from pydantic import BaseModel
from redis import Redis

from core.config import settings
from schemas.movies import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MovieUpdatePartial,
)
from storage.movies.exceptions import MovieAlreadyExistsError

log = logging.getLogger(__name__)
redis_movie = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.movie,
    decode_responses=True,
)


class MovieStorage(BaseModel):
    hash_name: str

    def save_movie(self, movie: Movie) -> None:
        redis_movie.hset(
            name=self.hash_name,
            key=movie.slug,
            value=movie.model_dump_json(),
        )
        log.info("Saved movie to redis storage")

    def get(self) -> list[Movie]:
        if movies := cast(
            Iterable[str],
            redis_movie.hvals(
                name=self.hash_name,
            ),
        ):
            return [Movie.model_validate_json(movie) for movie in movies]
        return []

    def get_by_slug(self, slug: str) -> Movie | None:
        movie = cast(
            str,
            redis_movie.hget(
                name=self.hash_name,
                key=slug,
            ),
        )
        return Movie.model_validate_json(movie) if movie else None

    def exists(self, slug: str) -> bool:
        return cast(
            bool,
            redis_movie.hexists(
                name=self.hash_name,
                key=slug,
            ),
        )

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.save_movie(movie)
        log.info("Created movie with slug '%s'", movie.slug)
        return movie

    def create_or_raise_if_exists(self, movie_in: MovieCreate) -> Movie:
        if not self.exists(movie_in.slug):
            return self.create(movie_in=movie_in)

        raise MovieAlreadyExistsError(movie_in.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis_movie.hdel(
            self.hash_name,
            slug,
        )

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movie(movie)
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MovieUpdatePartial,
    ) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_movie(movie)
        return movie


storage = MovieStorage(
    hash_name=settings.redis.collections_names.movie_hash,
)
