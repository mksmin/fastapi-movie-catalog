from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
)

from api.api_v1.movies.crud import storage
from schemas.movies import Movie, MovieCreate, MovieRead

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[MovieRead],
)
def get_movies() -> list[Movie]:
    return storage.get()


@router.post("/", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_create: MovieCreate,
    background_tasks: BackgroundTasks,
) -> Movie:
    movie = storage.create(movie_create)
    background_tasks.add_task(storage.save_state)
    return movie
