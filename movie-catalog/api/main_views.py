from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter()


@router.get(
    "/",
    include_in_schema=False,
)
def read_root(
    request: Request,
) -> HTMLResponse:
    context = {}
    features = [
        "Показ рейтинга фильмов",
        "Подробная информация о фильме",
    ]
    context.update(
        features=features,
    )

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )


@router.get(
    "/about",
    include_in_schema=False,
)
def about_page(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )
