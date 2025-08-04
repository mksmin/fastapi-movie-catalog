from fastapi import (
    APIRouter,
    status,
)

from api.api_v1.movies.crud import storage
from schemas.movies import Movie, MovieCreateSchema

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def get_movies() -> list[Movie]:
    return storage.get()


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_create: MovieCreateSchema,
) -> Movie:
    return storage.create(movie_create)
