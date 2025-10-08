from collections.abc import Mapping
from typing import Any

from fastapi import (
    APIRouter,
    Request,
    status,
)
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)
from pydantic import BaseModel, ValidationError

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


def format_pydantic_error(
    error: ValidationError,
) -> dict[str, str]:
    return {str(err["loc"][0]): err["msg"] for err in error.errors()}


def create_view_validation_response(
    request: Request,
    errors: dict[str, str] | None = None,
    form_data: BaseModel | Mapping[str, Any] | None = None,
    *,
    form_validated: bool = True,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = MovieCreate.model_json_schema()
    context.update(
        model_schema=model_schema,
        errors=errors,
        form_validated=form_validated,
        form_data=form_data,
    )
    return templates.TemplateResponse(
        request=request,
        name="movies/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
            errors = format_pydantic_error(e)
            return create_view_validation_response(
                request=request,
                errors=errors,
                form_data=form,
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
        return RedirectResponse(
            url=request.url_for("movies:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return create_view_validation_response(
        request=request,
        errors=errors,
        form_data=movie_create,
    )
