from fastapi import APIRouter, Request, status
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)
from pydantic import ValidationError

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
    response_model=None,
)
async def update_movie(
    request: Request,
    movie: MovieBySlug,
    storage: GetMoviesStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            movie_in = MovieUpdateForm.model_validate(form)
        except ValidationError as e:
            return form_response.render(
                request=request,
                form_data=form,
                form_validated=True,
                pydantic_error=e,
                movie=movie,
            )

    storage.update(movie, movie_in)
    return RedirectResponse(
        url=request.url_for("movies:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
