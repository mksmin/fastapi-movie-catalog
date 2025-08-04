from pydantic import BaseModel
from schemas.movies import Movie, MovieCreateSchema


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie: MovieCreateSchema) -> Movie:
        movie = Movie(
            **movie.model_dump(),
        )
        self.slug_to_movie[movie.slug] = movie
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)


storage = MovieStorage()

storage.create(
    MovieCreateSchema(
        slug="ring_owner",
        title="Властелин Колец",
        description="""Храбрый хоббит Фродо Бэггинс женился на дочери короля Саурон.""",
        rating=9,
    )
)
storage.create(
    MovieCreateSchema(
        slug="shawshank_redemption",
        title="Побег из Шоушенка",
        description="""Джон Трэйси — молодой драматург, который обрел многое от своей мечты в жизни.""",
        rating=7,
    )
)
storage.create(
    MovieCreateSchema(
        slug="spiderman",
        title="Человек-паук",
        description="""Странный парень в красном костюме мешает жить людям стреляя в них пауками.""",
        rating=8,
    )
)
