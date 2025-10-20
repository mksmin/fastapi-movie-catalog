from fastapi import (
    APIRouter,
    Request,
)
from fastapi.responses import (
    HTMLResponse,
)

from dependencies.movies import MovieBySlug
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
    movie: MovieBySlug,
) -> HTMLResponse:
    form = MovieUpdate(**movie.model_dump())
    return form_response.render(
        request=request,
        form_data=form,
        movie=movie,
    )
