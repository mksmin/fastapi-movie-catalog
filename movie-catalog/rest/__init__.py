from fastapi import APIRouter

from rest.main_views import router as main_views_router
from rest.movies import router as movies_views_router

router = APIRouter(
    # include_in_schema=False,
)
router.include_router(
    main_views_router,
)
router.include_router(
    movies_views_router,
)
