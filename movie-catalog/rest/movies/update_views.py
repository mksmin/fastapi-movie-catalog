from typing import Annotated

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)

from dependencies.movies import GetMoviesStorage, MovieBySlug
from schemas.movies import MovieUpdate, MovieUpdateForm
from services.movies import FormResponseHelper

router = APIRouter(
    prefix="/{slug}/update",
)

form_response = FormResponseHelper(
    model=MovieUpdateForm,
    template_name="movies/update.html",
)


@router.get(
    "/",
    name="movies:update-view",
)
def get_page_create_movie(
    request: Request,
    movie: MovieBySlug,
) -> HTMLResponse:
    form = MovieUpdate(**movie.model_dump())
    return form_response.render(
        request=request,
        form_data=form,
        movie=movie,
    )


@router.post(
    "/",
    name="movies:update",
)
async def update_movie(
    request: Request,
    movie: MovieBySlug,
    movie_in: Annotated[
        MovieUpdateForm,
        Form(),
    ],
    storage: GetMoviesStorage,
) -> RedirectResponse:
    storage.update(movie, movie_in)
    return RedirectResponse(
        url=request.url_for("movies:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
