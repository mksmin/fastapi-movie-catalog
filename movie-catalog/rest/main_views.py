from typing import Any

from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter(
    include_in_schema=False,
)


@router.get(
    "/",
    name="home",
    include_in_schema=False,
)
def home_page(
    request: Request,
) -> HTMLResponse:
    context: dict[str, Any] = {}
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
    name="about",
    include_in_schema=False,
)
def about_page(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )
