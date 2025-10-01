from datetime import date

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
    today = date.today()
    features = [
        "Показ рейтинга фильмов",
        "Подробная информация о фильме",
    ]
    context.update(
        today=today,
        features=features,
    )

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )
