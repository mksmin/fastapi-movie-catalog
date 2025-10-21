from fastapi import (
    APIRouter,
    Request,
    status,
)
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)
from pydantic import ValidationError

from dependencies.movies import GetMoviesStorage
from schemas.movies import MovieCreate
from services.movies import FormResponseHelper
from storage.movies.exceptions import MovieAlreadyExistsError

router = APIRouter(
    prefix="/create",
)

form_response = FormResponseHelper(
    model=MovieCreate,
    template_name="movies/create.html",
)


@router.get(
    "/",
    name="movies:create-view",
)
def get_page_create_movie(
    request: Request,
) -> HTMLResponse:
    return form_response.render(
        request=request,
    )


@router.post(
    "/",
    name="movies:create",
    response_model=None,
)
async def create_movie(
    request: Request,
    storage: GetMoviesStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            movie_create = MovieCreate.model_validate(form)
        except ValidationError as e:
            return form_response.render(
                request=request,
                form_data=form,
                pydantic_error=e,
                form_validated=True,
            )
    try:
        storage.create_or_raise_if_exists(
            movie_create,
        )
    except MovieAlreadyExistsError:
        errors = {
            "slug": f"Movie with slug {movie_create.slug} already exists.",
        }
    else:
        request.session["message"] = f"Movie {movie_create.title!r} created."
        return RedirectResponse(
            url=request.url_for("movies:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return form_response.render(
        request=request,
        errors=errors,
        form_data=movie_create,
        form_validated=True,
    )
