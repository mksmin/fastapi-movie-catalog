import logging
from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import USER_DATA_STORAGE_FILEPATH
from schemas.movies import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MovieUpdatePartial,
    MovieRead,
)

log = logging.getLogger(__name__)
redis_movie = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_MOVIE_DB,
    decode_responses=True,
)


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_state(self) -> None:
        USER_DATA_STORAGE_FILEPATH.write_text(
            self.model_dump_json(indent=4),
            encoding="utf-8",
        )
        log.info("Saved state to storage file")

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not USER_DATA_STORAGE_FILEPATH.exists():
            log.info("Movie storage file doesn't exist")
            return MovieStorage()
        return cls.model_validate_json(
            USER_DATA_STORAGE_FILEPATH.read_text(
                encoding="utf-8",
            )
        )

    def init_storage_from_state(self):
        try:
            data = MovieStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error")
            return

        self.slug_to_movie.update(
            data.slug_to_movie,
        )
        log.warning("Recovered data from storage file.")

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        movie = redis_movie.hget(
            name=config.REDIS_MOVIE_HASH_NAME,
            key=slug,
        )
        return Movie.model_validate_json(movie) if movie else None

    def create(self, movie: MovieCreate) -> Movie:
        movie = Movie(
            **movie.model_dump(),
        )
        redis_movie.hset(
            name=config.REDIS_MOVIE_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )
        log.info("Created movie with slug '%s'", movie.slug)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MovieUpdatePartial,
    ) -> Movie:
        movie = self.get_by_slug(movie.slug)

        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
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
