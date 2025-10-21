from fastapi import (
    APIRouter,
    status,
)
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from dependencies.movies import GetMoviesStorage, MovieBySlug

router = APIRouter(
    prefix="/{slug}/delete",
)


@router.post(
    "/",
    name="movies:delete",
)
def delete_movie(
    request: Request,
    movie: MovieBySlug,
    storage: GetMoviesStorage,
) -> RedirectResponse:
    storage.delete(movie)
    return RedirectResponse(
        url=request.url_for("movies:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
