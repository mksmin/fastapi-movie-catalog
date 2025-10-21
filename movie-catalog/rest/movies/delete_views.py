from fastapi import (
    APIRouter,
    status,
)
from starlette.responses import Response

from dependencies.movies import GetMoviesStorage, MovieBySlug

router = APIRouter(
    prefix="/{slug}/delete",
)


@router.delete(
    "/",
    name="movies:delete",
)
def delete_movie(
    movie: MovieBySlug,
    storage: GetMoviesStorage,
) -> Response:
    storage.delete(movie)
    return Response(
        status_code=status.HTTP_200_OK,
        content="",
    )
