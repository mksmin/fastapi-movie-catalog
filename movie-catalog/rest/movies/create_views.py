from typing import Annotated, Any

from fastapi import APIRouter, Form

from schemas.movies import MovieCreate

router = APIRouter(
    prefix="/create",
)


@router.get(
    "/",
    name="",
)
def get_page_create_movie() -> None:
    pass


@router.post("/", name="")
def create_movie(
    movie_create: Annotated[
        MovieCreate,
        Form(),
    ],
) -> dict[str, Any]:
    return movie_create.model_dump(mode="json")
