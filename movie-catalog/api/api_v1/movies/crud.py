from pathlib import Path
from pydantic import BaseModel
from pydantic_core import from_json

from core.config import USER_DATA_STORAGE_DIR as DATADIR
from schemas.movies import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MovieUpdatePartial,
    MovieRead,
)


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def _get_file_path(self, slug: str) -> Path | None:
        return DATADIR / f"{slug}.json"

    def file_is_exist(self, slug: str) -> bool:
        file_path = self._get_file_path(slug)
        return file_path.exists()

    def get(self) -> list[Movie]:
        for file in DATADIR.glob("*.json"):
            try:
                movie_json = from_json(file.read_text(encoding="utf-8"))
                movie = Movie.model_validate(movie_json)
                self.slug_to_movie[movie.slug] = movie
            except ValueError:
                continue
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        if not self.file_is_exist(slug):
            return None

        file_path = self._get_file_path(slug)
        movie_json = from_json(file_path.read_text(encoding="utf-8"))
        movie = Movie.model_validate(movie_json)
        return movie

    def create(self, movie: MovieCreate) -> Movie:
        file_path = self._get_file_path(movie.slug)
        if not self.file_is_exist(movie.slug):
            file_path.touch(exist_ok=True)

        movie = Movie(
            **movie.model_dump(),
        )
        movie_json = movie.model_dump_json(indent=4)
        file_path.write_text(movie_json, encoding="utf-8")
        return movie

    def delete_by_slug(self, slug: str) -> None:
        if not self.file_is_exist(slug):
            return None

        file_path = self._get_file_path(slug)
        file_path.unlink(missing_ok=True)
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        movie = self.get_by_slug(movie.slug)

        for field_name, value in movie_in:
            setattr(movie, field_name, value)

        file_path = self._get_file_path(movie.slug)
        file_path.write_text(movie.model_dump_json(indent=4), encoding="utf-8")

        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MovieUpdatePartial,
    ) -> Movie:
        movie = self.get_by_slug(movie.slug)

        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)

        file_path = self._get_file_path(movie.slug)
        file_path.write_text(movie.model_dump_json(indent=4), encoding="utf-8")

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
