from typing import Annotated

import uvicorn
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
from schemas.movies import Movie

app = FastAPI(title="Movie Catalog")


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }


MOVIES = [
    Movie(
        id=1,
        title="Властелин Колец",
        description="""Храбрый хоббит Фродо Бэггинс женился на дочери короля Саурон.""",
        rating=9.5,
    ),
    Movie(
        id=2,
        title="Побег из Шоушенка",
        description="""Джон Трэйси — молодой драматург, который обрел многое от своей мечты в жизни.""",
        rating=7.3,
    ),
    Movie(
        id=3,
        title="Человек-паук",
        description="""Странный парень в красном костюме мешает жить людям стреляя в них пауками.""",
        rating=8.2,
    ),
]


def get_movie_by_id(
    movie_id: int,
):
    movie: Movie | None = next(
        (movie for movie in MOVIES if movie.id == movie_id),
        None,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Movie not found",
    )


@app.get(
    "/movies/",
    response_model=list[Movie],
)
def get_movies():
    return MOVIES


@app.get(
    "/movies/{movie_id}",
    response_model=Movie,
)
def get_movie(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_id),
    ],
):
    return movie


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
