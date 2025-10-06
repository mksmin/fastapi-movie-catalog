from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Form,
    Request,
    status,
)
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)

from dependencies.movies import GetMoviesStorage
from schemas.movies import MovieCreate
from storage.movies.exceptions import MovieAlreadyExistsError
from templating import templates

router = APIRouter(
    prefix="/create",
)


@router.get(
    "/",
    name="movies:create-view",
)
def get_page_create_movie(
    request: Request,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = MovieCreate.model_json_schema()
    context.update(
        model_schema=model_schema,
    )
    return templates.TemplateResponse(
        request=request,
        name="movies/create.html",
        context=context,
    )


@router.post(
    "/",
    name="movies:create",
    response_model=None,
)
def create_movie(
    request: Request,
    movie_create: Annotated[
        MovieCreate,
        Form(),
    ],
    storage: GetMoviesStorage,
) -> RedirectResponse | HTMLResponse:
    try:
        storage.create_or_raise_if_exists(
            movie_create,
        )
    except MovieAlreadyExistsError:
        errors = {
            "slug": f"Movie with slug {movie_create.slug} already exists.",
        }
    else:
        return RedirectResponse(
            url=request.url_for("movies:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    context: dict[str, Any] = {}
    model_schema = MovieCreate.model_json_schema()
    context.update(
        model_schema=model_schema,
        errors=errors,
        form_validated=True,
        form_data=movie_create,
    )
    return templates.TemplateResponse(
        request=request,
        name="movies/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
