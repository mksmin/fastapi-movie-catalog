from schemas.movies import Movie

MOVIES = [
    Movie(
        slug="ring_owner",
        title="Властелин Колец",
        description="""Храбрый хоббит Фродо Бэггинс женился на дочери короля Саурон.""",
        rating=9.5,
    ),
    Movie(
        slug="shawshank_redemption",
        title="Побег из Шоушенка",
        description="""Джон Трэйси — молодой драматург, который обрел многое от своей мечты в жизни.""",
        rating=7.3,
    ),
    Movie(
        slug="spiderman",
        title="Человек-паук",
        description="""Странный парень в красном костюме мешает жить людям стреляя в них пауками.""",
        rating=8.2,
    ),
]
