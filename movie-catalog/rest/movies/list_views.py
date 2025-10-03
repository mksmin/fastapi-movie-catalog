from typing import Any

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from templating import templates

router = APIRouter()


@router.get(
    "/",
    name="movies:list",
    response_class=HTMLResponse,
)
def list_views(
    request: Request,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    movies = []
    context.update(
        movies=movies,
    )
    return templates.TemplateResponse(
        request=request,
        name="movies/list.html",
        context=context,
    )
