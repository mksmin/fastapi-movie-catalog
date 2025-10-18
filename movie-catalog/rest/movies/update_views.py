from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import (
    HTMLResponse,
)

from schemas.movies import MovieUpdate
from services.movies import FormResponseHelper

router = APIRouter(
    prefix="/{slug}/update",
)

form_response = FormResponseHelper(
    model=MovieUpdate,
    template_name="movies/update.html",
)


@router.get(
    "/",
    name="movies:update-view",
)
def get_page_create_movie(
    request: Request,
) -> HTMLResponse:
    return form_response.render(
        request=request,
    )
