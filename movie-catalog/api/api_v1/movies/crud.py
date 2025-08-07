import logging
from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.movies import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MovieUpdatePartial,
)

log = logging.getLogger(__name__)
redis_movie = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_MOVIE_DB,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """
    Base exception for movie CRUD actions
    """


class MovieAlreadyExistsError(MovieBaseError):
    """
    Raised on movie creation if such slug already exists
    """


class MovieStorage(BaseModel):
    def save_movie(self, movie: Movie) -> None:
        redis_movie.hset(
            name=config.REDIS_MOVIE_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )
        log.info("Saved movie to redis storage")

    def get(self) -> list[Movie]:
        if movies := redis_movie.hvals(
            name=config.REDIS_MOVIE_HASH_NAME,
        ):
            result = [Movie.model_validate_json(movie) for movie in movies]
            return result
        return []

    def get_by_slug(self, slug: str) -> Movie | None:
        movie = redis_movie.hget(
            name=config.REDIS_MOVIE_HASH_NAME,
            key=slug,
        )
        return Movie.model_validate_json(movie) if movie else None

    def exists(self, slug: str) -> bool:
        return redis_movie.hexists(
            name=config.REDIS_MOVIE_HASH_NAME,
            key=slug,
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
            config.REDIS_MOVIE_HASH_NAME,
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


storage = MovieStorage()


# storage.create(
#     MovieCreate(
#         slug="ring_owner",
#         title="Властелин Колец",
#         description="""Храбрый хоббит Фродо Бэггинс женился на дочери короля Саурон.""",
#         rating=9,
#     )
# )
# storage.create(
#     MovieCreate(
#         slug="shawshank_redemption",
#         title="Побег из Шоушенка",
#         description="""Джон Трэйси — молодой драматург, который обрел многое от своей мечты в жизни.""",
#         rating=7,
#     )
# )
# storage.create(
#     MovieCreate(
#         slug="spiderman",
#         title="Человек-паук",
#         description="""Странный парень в красном костюме мешает жить людям стреляя в них пауками.""",
#         rating=8,
#     )
# )
