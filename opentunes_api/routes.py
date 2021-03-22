from fastapi import APIRouter

from opentunes_api.routers import tracks

router = APIRouter()
router.include_router(router=tracks.router, tags=["tracks"], prefix="/api/tracks")
