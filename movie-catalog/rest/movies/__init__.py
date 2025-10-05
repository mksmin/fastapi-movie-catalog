from fastapi import APIRouter

from rest.movies.create_views import router as create_views_router
from rest.movies.list_views import router as list_views_router

router = APIRouter(
    tags=["Movies rest"],
    prefix="/movies",
)

router.include_router(
    list_views_router,
)
router.include_router(
    create_views_router,
)
