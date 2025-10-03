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
    return templates.TemplateResponse(
        request=request,
        name="movies/list.html",
    )
